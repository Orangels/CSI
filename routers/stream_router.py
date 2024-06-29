from fastapi import APIRouter, Request, WebSocketDisconnect, WebSocket
from fastapi.responses import StreamingResponse
import ffmpeg
import asyncio
import requests
import os
import signal

router = APIRouter()


@router.get("/api/stream/rtsp")
async def stream_video(url: str, request: Request):
    process = (
        ffmpeg.input(url)
        .output("pipe:1", format="flv", codec="copy")
        .global_args("-re")
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )

    async def video_stream():
        try:
            while True:

                if await request.is_disconnected():
                    print("断开连接")
                    process.terminate()
                    break
                chunk = await asyncio.to_thread(process.stdout.read, 4096)
                if not chunk:
                    break
                yield chunk
        except Exception as e:
            process.terminate()
            raise e

    return StreamingResponse(video_stream(), media_type="video/x-flv")


@router.websocket("/api/stream/rtspws")
async def websocket_stream(websocket: WebSocket, url: str):
    await websocket.accept()
    process = (
        ffmpeg.input(url)
        .output("pipe:1", format="flv", codec="copy")
        .global_args("-re")
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )
    try:
        while process.poll() is None:
            try:
                packet = await asyncio.wait_for(
                    asyncio.to_thread(process.stdout.readline), 1000
                )
            except:
                print("timeout")
                packet = b''
            if not packet:
                print("packet is None")
            await websocket.send_bytes(packet)
        
        print("process end")
    except WebSocketDisconnect:
        print("WebSocketDisconnect")
    except asyncio.TimeoutError:
        print("timeout")
    except Exception as e:
        print(f"unknown error: {e}")
    finally:
        process.stdout.close()
        process.stderr.close()
        process.terminate()
        os.kill(process.pid, signal.SIGTERM)
        process.wait()
        await websocket.close()
    print("over")

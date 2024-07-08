from fastapi import APIRouter, Request, WebSocketDisconnect, WebSocket
from fastapi.responses import StreamingResponse
import ffmpeg
import asyncio

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
    command = [
        "ffmpeg",
        "-i",
        url,  # Input
        "-rtsp_transport",
        "tcp",
        "-f",
        "flv",  # Output format
        "-c",
        "copy",  # Codec
        "pipe:",  # Output to stdout
    ]

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        while True:
            packet = await process.stdout.read(8192)
            if not packet:
                print("packet is none")
                await websocket.send_bytes(b'\x00\x00\x00\x00')
                break
            await websocket.send_bytes(packet)
    except WebSocketDisconnect:
        print("WebSocketDisconnect")
    except asyncio.TimeoutError:
        print("asyncio timeout")
    except Exception as e:
        print(f"unknown error: {e}")
    finally:
        process.terminate()
        await process.wait()
        await websocket.close()

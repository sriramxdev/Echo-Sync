# tests/manual/run_ui_preview.py
"""Starts the Stage 1 Ingestion Broadcaster for live WebSocket UI testing."""

from src.ingestion import RawHolisticIngestor, IngestionBroadcaster


def main() -> None:
    ingestor = RawHolisticIngestor(camera_id=0, model_complexity=0, include_image=True)
    hub = IngestionBroadcaster(ingestor, ws_port=8765).start(enable_ws=True)

    print("[*] Stage 1 Broadcaster active at ws://127.0.0.1:8765")
    print("[*] Open tests/manual/test_ui_client.html in your browser.")
    print("[*] Press Ctrl+C to stop.")

    try:
        while True:
            # Drain internal ML queue just as Stage 2 (DynaPrune) will
            hub.get_latest_packet(timeout=0.5)
    except KeyboardInterrupt:
        print("\n[*] Shutting down Stage 1 Broadcaster...")
    finally:
        hub.stop()
        print("[SUCCESS] Clean shutdown.")


if __name__ == "__main__":
    main()
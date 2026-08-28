type MessageCallback = (data: string) => void;

class WebSocketService {
  private ws: WebSocket | null = null;
  private callbacks: MessageCallback[] = [];
  private reconnectTimer: number | null = null;
  public isConnected = false;

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN) return;

    this.ws = new WebSocket('ws://localhost:8000/ws');

    this.ws.onopen = () => {
      this.isConnected = true;
      console.log('WebSocket connected');
      this.notifyStatusChange();
    };

    this.ws.onmessage = (event) => {
      this.callbacks.forEach(cb => cb(event.data));
    };

    this.ws.onclose = () => {
      this.isConnected = false;
      this.notifyStatusChange();
      console.log('WebSocket disconnected. Reconnecting in 3s...');
      this.reconnectTimer = window.setTimeout(() => this.connect(), 3000);
    };

    this.ws.onerror = (err) => {
      console.error('WebSocket error:', err);
      this.ws?.close();
    };
  }

  private notifyStatusChange() {
    this.callbacks.forEach(cb => cb(JSON.stringify({ type: 'WS_STATUS', connected: this.isConnected })));
  }

  subscribe(callback: MessageCallback) {
    this.callbacks.push(callback);
    return () => {
      this.callbacks = this.callbacks.filter(cb => cb !== callback);
    };
  }

  send(data: string) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(data);
    }
  }

  disconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.ws?.close();
  }
}

export const wsService = new WebSocketService();

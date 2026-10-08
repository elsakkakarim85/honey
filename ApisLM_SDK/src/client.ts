import axios, { AxiosInstance } from 'axios';
import { EdgeTelemetry, SwarmPrediction } from './types/iot';
import { DigitalProductPassport } from './types/dpp';

export interface ApisLMClientConfig {
  apiKey: string;
  edgeBaseUrl?: string;
  cloudBaseUrl?: string;
}

export class ApisLMClient {
  private edgeClient: AxiosInstance;
  private cloudClient: AxiosInstance;

  constructor(config: ApisLMClientConfig) {
    this.edgeClient = axios.create({
      baseURL: config.edgeBaseUrl || 'http://localhost:8000/api/iot',
      headers: { 'Authorization': `Bearer ${config.apiKey}` }
    });

    this.cloudClient = axios.create({
      baseURL: config.cloudBaseUrl || 'https://api.apislm.com/v1',
      headers: { 'Authorization': `Bearer ${config.apiKey}` }
    });
  }

  /**
   * Post raw edge telemetry from a local IoT node (e.g. ESP32 via bridge)
   */
  async ingestTelemetry(payload: EdgeTelemetry): Promise<boolean> {
    const res = await this.edgeClient.post('/ingest', payload);
    return res.status === 200 || res.status === 201;
  }

  /**
   * Request a real-time Swarm Prediction from the local Llama-3 model
   */
  async getSwarmPrediction(hiveId: string): Promise<SwarmPrediction> {
    const res = await this.edgeClient.get(`/predict/swarm/${hiveId}`);
    return res.data as SwarmPrediction;
  }

  /**
   * Sync local edge data to the cloud tenant
   */
  async triggerCloudSync(): Promise<{ syncedRecords: number }> {
    const res = await this.cloudClient.post('/sync/upstream');
    return res.data;
  }
}

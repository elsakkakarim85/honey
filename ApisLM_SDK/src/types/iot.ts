export interface EdgeTelemetry {
  deviceId: string;
  timestampMs: number;
  sensors: {
    broodTempC: number;
    humidityRh: number;
    weightKg: number;
    acousticHz: number;
  };
  metrics: {
    batteryLevelPct: number;
    signalStrengthDbm: number;
  };
}

export interface SwarmPrediction {
  hiveId: string;
  probability: number;
  estimatedTimeframeHours: number;
  primaryTriggers: string[];
}

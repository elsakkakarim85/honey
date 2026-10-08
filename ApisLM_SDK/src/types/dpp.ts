export interface DigitalProductPassport {
  batchId: string;
  apiaryLocation: {
    lat: number;
    lng: number;
    name: string;
  };
  harvestDate: string;
  floralSource: string[];
  metrics: {
    moisturePercent: number;
    totalWeightKg: number;
  };
  signature?: string; // Ed25519 Cryptographic Signature
}

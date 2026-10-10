import { DigitalProductPassport } from './types/dpp';
import * as crypto from 'crypto';

/** Canonical JSON (sorted keys). Identical to the dashboard's `/api/dpp`, so signatures are reproducible across both. */
export function canonicalJson(v: any): string {
  if (Array.isArray(v)) return `[${v.map(canonicalJson).join(',')}]`;
  if (v && typeof v === 'object') return `{${Object.keys(v).filter(k => v[k] !== undefined).sort().map(k => `${JSON.stringify(k)}:${canonicalJson(v[k])}`).join(',')}}`;
  return JSON.stringify(v);
}

export class DPPGenerator {
  private privateKey: crypto.KeyObject;

  /** @param privateKeyPem Ed25519 private key, PKCS8 PEM. */
  constructor(privateKeyPem: string) {
    this.privateKey = crypto.createPrivateKey(privateKeyPem);
    if (this.privateKey.asymmetricKeyType !== 'ed25519') throw new Error('DPPGenerator requires an Ed25519 private key');
  }

  /** Generates an Ed25519-signed Digital Product Passport (signature is base64url over the canonical JSON of the data). */
  public generateSignedPassport(passportData: Omit<DigitalProductPassport, 'signature'>): DigitalProductPassport {
    const signature = crypto.sign(null, Buffer.from(canonicalJson(passportData)), this.privateKey).toString('base64url');
    return { ...passportData, signature };
  }

  /** Verifies a passport against an Ed25519 public key (SPKI PEM). Returns false for any tampering or malformed input. */
  public static verifyPassport(passport: DigitalProductPassport, publicKeyPem: string): boolean {
    if (!passport || !passport.signature) return false;
    try {
      const { signature, ...data } = passport;
      return crypto.verify(null, Buffer.from(canonicalJson(data)), crypto.createPublicKey(publicKeyPem), Buffer.from(signature, 'base64url'));
    } catch {
      return false;
    }
  }
}

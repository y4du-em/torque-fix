export type FuelType = "petrol" | "diesel" | "electric" | "hybrid";
export type VehicleType = "bike" | "car" | "truck" | "scooter";
export type DifficultyLevel = "easy" | "medium" | "hard" | "professional";
export type SymptomCategory =
  | "engine"
  | "brakes"
  | "electrical"
  | "transmission"
  | "suspension"
  | "fuel"
  | "cooling"
  | "exhaust"
  | "other";

export interface VehicleContext {
  type: VehicleType;
  make: string;
  model: string;
  year: number;
  engineCC?: number;
  fuelType: FuelType;
  transmission?: "manual" | "automatic";
  mileage?: number;
}

export interface Tool {
  name: string;
  size?: string;
  type: string;
  required: boolean;
}

export interface Part {
  name: string;
  partNumber?: string;
  quantity: number;
  estimatedCost?: string;
  priority: "critical" | "recommended" | "optional";
}

export interface RepairStep {
  stepNumber: number;
  title: string;
  description: string;
  warning?: string;
  tip?: string;
  estimatedTime?: string;
}

export interface DiagnosisRequest {
  vehicle: VehicleContext;
  symptoms: string[];
  additionalNotes?: string;
}

export interface DiagnosisResponse {
  id: string;
  vehicle: VehicleContext;
  symptoms: string[];
  diagnosis: string;
  tools: Tool[];
  parts: Part[];
  steps: RepairStep[];
  difficulty: DifficultyLevel;
  estimatedTime: string;
  estimatedCost?: string;
  warningFlags: string[];
  safetyNotes: string[];
  createdAt: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
}

export interface ChatRequest {
  message: string;
  history: ChatMessage[];
  vehicleContext?: VehicleContext;
  diagnosisContext?: DiagnosisResponse;
}

export interface ApiError {
  message: string;
  code: string;
  statusCode: number;
}

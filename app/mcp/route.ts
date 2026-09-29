import { handleMcpRequest } from "@/lib/research/mcp";

export function GET(request: Request) {
  return handleMcpRequest(request);
}

export function POST(request: Request) {
  return handleMcpRequest(request);
}

export function OPTIONS(request: Request) {
  return handleMcpRequest(request);
}

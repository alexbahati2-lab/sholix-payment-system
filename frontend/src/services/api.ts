const API_BASE_URL = "/api";import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
export interface PaymentOrder {
  id: number;
  reference: string;
  direction: string;
  channel: string;
  amount: string | number;
  currency: string;
  customer_name?: string;
  customer_phone?: string;
  status: string;
  created_at: string;
}

export interface DashboardSummary {
  system: string;
  currency: string;
  businesses_count: number;
  payment_orders_count: number;
  pending_orders_count: number;
  processing_orders_count: number;
  successful_orders_count: number;
  failed_orders_count: number;
  successful_collection_orders_total: string;
  recent_orders: PaymentOrder[];
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  const response = await fetch(`${API_BASE_URL}/dashboard/`, {
    method: "GET",
    credentials: "include",
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      throw new Error(
        "Authentication required. Sign in to Django admin in this browser, then refresh."
      );
    }

    throw new Error(`Dashboard API request failed (${response.status}).`);
  }

  return response.json() as Promise<DashboardSummary>;
}
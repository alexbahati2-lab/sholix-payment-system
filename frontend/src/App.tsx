import { useEffect, useState } from "react";
import {
  getDashboardSummary,
  type DashboardSummary,
} from "./services/api";
import "./App.css";

function App() {
  const [dashboard, setDashboard] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadDashboard() {
    setLoading(true);
    setError("");

    try {
      const data = await getDashboardSummary();
      setDashboard(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Could not load the dashboard."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadDashboard();
  }, []);

  const money = (amount: string | number, currency = "KES") =>
    new Intl.NumberFormat("en-KE", {
      style: "currency",
      currency,
      maximumFractionDigits: 2,
    }).format(Number(amount));

  const stats = dashboard
    ? [
        { label: "Businesses", value: dashboard.businesses_count },
        { label: "Payment orders", value: dashboard.payment_orders_count },
        { label: "Pending", value: dashboard.pending_orders_count },
        { label: "Processing", value: dashboard.processing_orders_count },
        { label: "Successful", value: dashboard.successful_orders_count },
        { label: "Failed", value: dashboard.failed_orders_count },
      ]
    : [];

  return (
    <main className="dashboard">
      <header className="topbar">
        <div>
          <p className="eyebrow">PAYMENTS & COLLECTIONS</p>
          <h1>Sholix Payment System</h1>
          <p className="muted">Your business payment dashboard</p>
        </div>
        <button onClick={() => void loadDashboard()} disabled={loading}>
          {loading ? "Loading..." : "Refresh"}
        </button>
      </header>

      {loading && <p className="notice">Loading dashboard data...</p>}

      {error && (
        <section className="error-panel">
          <h2>Unable to load dashboard</h2>
          <p>{error}</p>
          <button onClick={() => void loadDashboard()}>Try again</button>
        </section>
      )}

      {dashboard && !error && (
        <>
          <section className="summary-panel">
            <div>
              <p className="muted">Successful collection orders total</p>
              <h2>
                {money(
                  dashboard.successful_collection_orders_total,
                  dashboard.currency
                )}
              </h2>
              <p className="muted">
                Based on successful orders currently recorded in SPS.
              </p>
            </div>
            <span className="status-pill">API Connected</span>
          </section>

          <section className="stats-grid">
            {stats.map((stat) => (
              <article className="stat-card" key={stat.label}>
                <p className="muted">{stat.label}</p>
                <h2>{stat.value.toLocaleString()}</h2>
              </article>
            ))}
          </section>

          <section className="orders-panel">
            <div className="section-heading">
              <div>
                <h2>Recent payment orders</h2>
                <p className="muted">Your latest recorded orders</p>
              </div>
            </div>

            {dashboard.recent_orders.length === 0 ? (
              <p className="notice">
                No payment orders yet. Orders will appear here when recorded.
              </p>
            ) : (
              <div className="table-scroll">
                <table>
                  <thead>
                    <tr>
                      <th>Reference</th>
                      <th>Customer</th>
                      <th>Channel</th>
                      <th>Amount</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dashboard.recent_orders.map((order) => (
                      <tr key={order.id}>
                        <td>{order.reference}</td>
                        <td>
                          {order.customer_name ||
                            order.customer_phone ||
                            "—"}
                        </td>
                        <td>{order.channel}</td>
                        <td>{money(order.amount, order.currency)}</td>
                        <td>
                          <span
                            className={`order-status ${order.status.toLowerCase()}`}
                          >
                            {order.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </>
      )}
    </main>
  );
}

export default App;
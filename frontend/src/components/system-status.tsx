"use client";

import { useEffect, useState } from "react";

type ApiState = "checking" | "online" | "offline";

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export function SystemStatus() {
  const [state, setState] = useState<ApiState>("checking");

  useEffect(() => {
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 3000);

    async function checkApi() {
      try {
        const response = await fetch(`${apiUrl}/health`, {
          cache: "no-store",
          signal: controller.signal,
        });
        setState(response.ok ? "online" : "offline");
      } catch {
        setState("offline");
      } finally {
        window.clearTimeout(timeout);
      }
    }

    void checkApi();
    return () => {
      window.clearTimeout(timeout);
      controller.abort();
    };
  }, []);

  const label = {
    checking: "Checking backend",
    online: "Backend online",
    offline: "Backend offline",
  }[state];

  return (
    <div className={`system-status system-status--${state}`} title={`API: ${apiUrl}`}>
      <span className="status-dot" /> {label}
    </div>
  );
}

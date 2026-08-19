/**
 * Placeholder home page.
 *
 * The real home page is Phase 16: four domain cards and example topics, following
 * decision F-01 (topic first, then map). Nothing here is final design work — Phase 5
 * only proves the app builds and can reach the API.
 */

async function getApiStatus(): Promise<string> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  try {
    const response = await fetch(`${apiUrl}/health/live`, { cache: "no-store" });
    return response.ok ? "connected" : `error ${response.status}`;
  } catch {
    return "not reachable";
  }
}

export default async function HomePage() {
  const apiStatus = await getApiStatus();

  return (
    <main>
      <h1>Internet Atlas</h1>
      <p>Explore the technology ecosystem as a map, not a list.</p>

      <section>
        <h2>Setup status</h2>
        <dl>
          <dt>Web app</dt>
          <dd>running</dd>
          <dt>API</dt>
          <dd>{apiStatus}</dd>
        </dl>
      </section>

      <footer>
        <p>Phase 5 — repository and standards. The product starts at Phase 14.</p>
      </footer>
    </main>
  );
}

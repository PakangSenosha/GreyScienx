import { Brand } from "@/components/Brand";
import { CasinoDataLink, CasinoNav } from "./CasinoNav";

export function CasinoShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="vc-shell">
      <a className="skip-link" href="#experiment-content">Skip to experiment content</a>
      <div className="vc-safety-ribbon" role="note">
        Research simulation · fictional money · no deposits, prizes or visitor wagers
      </div>
      <header className="vc-header">
        <Brand division="Virtual Casino Research" />
        <CasinoNav />
        <CasinoDataLink />
      </header>
      <main id="experiment-content" tabIndex={-1}>{children}</main>
      <footer className="vc-footer">
        <p><strong>GreyScienx</strong> · Virtual Casino Research</p>
        <p>Independent simulations. Published methods. Auditable results.</p>
      </footer>
    </div>
  );
}

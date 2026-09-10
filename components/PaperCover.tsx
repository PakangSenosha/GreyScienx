import type { ResearchPaper, Researcher } from "@/lib/types";

type PaperCoverProps = {
  paper: ResearchPaper;
  researcher: Researcher;
};

export function PaperCover({ paper, researcher }: PaperCoverProps) {
  if (paper.previewImage) {
    return (
      <img
        src={paper.previewImage}
        alt={`First page of ${paper.title} ${paper.titleAccent}`}
        width={816}
        height={1056}
      />
    );
  }

  return (
    <div className="paper-cover">
      <p className="paper-cover-kicker">GreyScienx · {paper.protocol}</p>
      <h2>
        {paper.title}
        <em> {paper.titleAccent}</em>
      </h2>
      <p className="paper-cover-by">{researcher.name}</p>
      <p className="paper-cover-aff">{researcher.affiliation}</p>
      <p className="paper-cover-dek">{paper.dek}</p>
      <div className="paper-cover-rule" />
      <p className="paper-cover-meta">
        {paper.field} · {paper.date}
      </p>
    </div>
  );
}

export interface GeneratePaperRequest {
  subject: string;
  grade: string;
  topics: string[];
  difficulty_distribution: {
    Easy: number;
    Medium: number;
    Hard: number;
  };
  question_types: string[];
}

export interface GeneratePaperResponse {
  status: 'success' | 'error';
  message: string;
  body: {
    paper: Record<string, string>;
    download_links: {
      pdf: string;
      word: string;
    };
  };
}

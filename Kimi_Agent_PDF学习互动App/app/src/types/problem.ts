export interface ProblemOption {
  label: string;
  value: string;
}

export interface Problem {
  id: number;
  question: string;
  image?: string;
  options: ProblemOption[];
  correctAnswer: string;
  points: number;
  hint: string;
  explanation: string[];
  keyConcept: string;
}

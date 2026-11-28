
import type { SearchResult } from "../types/search";

export const mockResults: SearchResult[] = [
  {
    id: "1",
    source: "03_work_from_home_policy.txt",
    text: "Employees may work remotely in accordance with company policy, subject to approval from their manager and applicable team requirements. Remote work arrangements must be coordinated with the employee's department.",
    score: 0.87,
  },
  {
    id: "2",
    source: "01_employee_handbook.txt",
    text: "Work arrangements and employee responsibilities are governed by the policies and guidelines established by the organization. Employees are expected to follow the applicable procedures.",
    score: 0.78,
  },
  {
    id: "3",
    source: "15_employee_faq.txt",
    text: "Employees should consult their manager or the HR department for additional information regarding remote work arrangements, flexibility and applicable internal procedures.",
    score: 0.72,
  },
];

export function getMockResults(query: string): SearchResult[] {
  return mockResults.map((result) => ({
    ...result,
    text: result.text,
  }));
}

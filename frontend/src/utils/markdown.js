import DOMPurify from "dompurify";
import { marked } from "marked";

marked.setOptions({
  breaks: false,
  gfm: true,
});

export function renderMarkdown(markdown = "") {
  const rawHtml = marked.parse(markdown || "");
  return DOMPurify.sanitize(rawHtml);
}

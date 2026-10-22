// Dates written out for the pages: "October 11th, 2026" from "2026-10-11". The family's rule
// for the prose a stranger reads (sentient-horizons/editorial/dates-in-prose.md, John
// 2026-10-21) writes a date the way it is said: month name, day with its ending, comma, year.
// The design standard writes dates out in the footer, and the tracker pattern
// (sentient-horizons/design/tracker-pattern.md, rule 5.2) writes the last-checked strip's date
// out too. Formatted from the date's own digits, so a date never shifts by a day with the
// machine's time zone. Data files, ids and file names keep year-month-day; only what is read
// on a page is spelled out.
const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

const ordinal = (d: number): string => {
  const rem100 = d % 100;
  if (rem100 >= 11 && rem100 <= 13) return `${d}th`;
  switch (d % 10) {
    case 1: return `${d}st`;
    case 2: return `${d}nd`;
    case 3: return `${d}rd`;
    default: return `${d}th`;
  }
};

export const longDate = (iso: string): string => {
  const [y, m, d] = iso.split('-').map(Number);
  if (!y || !m || !d || m < 1 || m > 12) return iso;
  return `${MONTHS[m - 1]} ${ordinal(d)}, ${y}`;
};

/**
 * Spell out every year-month-day date inside a run of prose: "Decided 2026-09-19." becomes
 * "Decided September 19th, 2026." A date that is part of something else is left alone: a file
 * path or address (docs/reviews/2026-09-19-rulings.md, data/scans/2026-10-08.toml), an id or
 * run key (2026-10-02-estimates-ruled), or a longer number. The data files carry the dates as
 * year-month-day, which is what makes them sortable and checkable; this is only how the page
 * reads them out.
 */
export const proseDates = (text: string | null | undefined): string => {
  if (!text) return '';
  return text.replace(
    /(^|[^\w/.-])(\d{4}-\d{2}-\d{2})(?![\w/-]|\.[A-Za-z])/g,
    (_m, before: string, iso: string) => before + longDate(iso),
  );
};

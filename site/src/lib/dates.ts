// Dates written out for the pages: "11 October 2026" from "2026-10-11". The design standard
// writes dates out in the footer, and the tracker pattern (sentient-horizons/design/tracker-pattern.md,
// rule 5.2) writes the last-checked strip's date out too. Formatted in UTC from the date's own
// digits, so a date never shifts by a day with the machine's time zone.
export const longDate = (iso: string): string => {
  const [y, m, d] = iso.split('-').map(Number);
  if (!y || !m || !d) return iso;
  return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' });
};

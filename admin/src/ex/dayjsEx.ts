import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";
import relativeTime from "dayjs/plugin/relativeTime";

export const timeZone = "Asia/Seoul";

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(relativeTime);
dayjs.tz.setDefault(timeZone);

export function safeDayjs(datetime: string | null | undefined): dayjs.Dayjs | undefined {
  if (datetime) {
    const m = dayjs(datetime);
    if (m.isValid()) {
      return m;
    }
  }
}

const FORMAT_ISO_DATE = "YYYY-MM-DD";

export function formatIsoDate(m: dayjs.Dayjs): string {
  return m.format(FORMAT_ISO_DATE);
}

export const betweenFormatIsoDateToString = (
  start: dayjs.Dayjs | null,
  end: dayjs.Dayjs | null,
): string => {
  if (!!start && !!end) {
    return `${formatIsoDate(start)} ~ ${formatIsoDate(end)}`;
  }
  return "";
};

export function now() {
  return dayjs();
}

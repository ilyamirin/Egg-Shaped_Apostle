// для сохранения рез-тов поиска
export interface FtsQuery {
  text: string;
  startDate: Date;
  endDate: Date;
  workplaces: number[];
  role: number;
}

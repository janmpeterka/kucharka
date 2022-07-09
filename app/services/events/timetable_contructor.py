from datetime import timedelta

from app.helpers.general import list_without_duplicated
from app.models import EventDay, DailyPlan


class TimetableContructor:
    def __init__(self, event):
        self.event = event

    # get active plans
    @property
    def event_daily_plans(self):
        return self.event.active_daily_plans

    # get events days
    @property
    def event_dates(self):
        return self.event.days

    # get task days
    @property
    def recipe_task_dates(self):
        dates = []
        for daily_plan in self.event_daily_plans:
            for daily_recipe in daily_plan.daily_recipes:
                for task in daily_recipe.recipe.tasks:
                    dates.append(
                        daily_plan.date + timedelta(days=(-task.days_before_cooking))
                    )
        return sorted(dates)

    @property
    def all_dates_with_agenda(self):

        dates = self.event_dates + self.recipe_task_dates

        return sorted(list_without_duplicated(dates))

    # add other week days
    @property
    def all_relevant_dates(self):
        first_date = self.all_dates_with_agenda[0]
        last_date = self.all_dates_with_agenda[-1]
        previous_monday = first_date + timedelta(days=-first_date.weekday())
        next_sunday = last_date + timedelta(days=-(last_date.weekday() + 1), weeks=1)

        return _date_range(previous_monday, next_sunday)

    @property
    def all_relevant_days(self):
        daily_plans = []
        for date in self.all_relevant_dates:
            daily_plan = DailyPlan.load_active_by_date_and_event(date, self.event)
            if daily_plan is None:
                daily_plan = EventDay(date=date, event=self.event)

            daily_plans.append(daily_plan)

        return daily_plans

    # split to weeks
    @property
    def all_relevant_days_split_by_weeks(self):
        lst = _chunks(self.all_relevant_days, 7)
        return lst

    def _weeks(self, dates) -> list:
        weeks = [date.week for date in dates]

        return list_without_duplicated(weeks)


def _date_range(start, end):
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def _chunks(lst, n):
    n = max(1, n)
    return [lst[i : i + n] for i in range(0, len(lst), n)]

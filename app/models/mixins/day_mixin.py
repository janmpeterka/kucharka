import datetime


class DayMixin:
    # DATA
    @property
    def all_tasks(self) -> list:
        tasks = []

        for daily_plan in self.event.daily_plans:
            if daily_plan.date >= self.date:
                for daily_recipe in daily_plan.daily_recipes:
                    tasks.extend(
                        task
                        for task in daily_recipe.tasks
                        if (
                            self.date
                            == daily_recipe.daily_plan.date
                            - datetime.timedelta(task.days_before_cooking)
                        )
                    )
        if hasattr(self, "tasks"):
            tasks.extend(self.tasks)

        return tasks

    @property
    def tasks_from_this_day(self) -> list:
        tasks = self.tasks

        for daily_recipe in self.daily_recipes:
            tasks = tasks + daily_recipe.recipe.tasks

        return tasks

    # PROPERTIES

    @property
    def is_active(self) -> bool:
        return self in self.event.active_daily_plans

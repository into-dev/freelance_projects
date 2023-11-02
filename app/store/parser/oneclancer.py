import aiohttp
from bs4 import BeautifulSoup
from app.store.parser.projectsparser import ProjectsParser


class OneCLancer(ProjectsParser):
    url: str = "https://1clancer.ru"
    projects: dict = {}

    async def get_projects(self):
        result = {}

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "lxml")
                    projects = soup.find_all("li", class_="answertask")

                    for project in projects:
                        project_id = project.get("rel")
                        p_link = project.find("a", class_="inlink")

                        project_title = p_link.text
                        project_url = self.url + p_link.get("href")
                        project_date = project.find("div", class_="date").text
                        project_customer = project.find("a", class_="customer").text

                        p_budget = project.find("div", class_="single-about")
                        if not p_budget:
                            p_budget = project.find("div", class_="all-about")
                        if not p_budget:
                            p_budget = project.find("div", class_="budg-cust")

                        if p_budget:
                            project_budget = p_budget.text
                        else:
                            project_budget = "Определяется исполнителем"

                        result[project_id] = {
                            "title": project_title,
                            "url": project_url,
                            "date": project_date,
                            "customer": project_customer,
                            "budget": project_budget,
                        }

        return result

    async def get_new_projects(self):
        result = {}
        projects = await self.get_projects()

        if self.projects:
            for project_id, project in projects.items():
                if project_id not in self.projects:
                    result[project_id] = project
        else:
            for project_id, project in projects.items():
                result[project_id] = project
                break

        self.projects = projects

        return result

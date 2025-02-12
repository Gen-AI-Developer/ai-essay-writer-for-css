from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class OutlineAndEssayCrew:
    """Poem Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def outline_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["outline_writer"],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def write_outline(self) -> Task:
        return Task(
            config=self.tasks_config["write_outline"],
        )

    @crew
    def outline_crew(self) -> Crew:
        """Creates the Research ouline on Given Topic"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=[self.outline_writer()],  # Automatically created by the @agent decorator
            tasks=[self.write_outline()],  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
    
    @agent
    def essay_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["essay_writer"],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def write_essay(self) -> Task:
        return Task(
            config=self.tasks_config["write_essay"],
        )

    @crew
    def essay_crew(self) -> Crew:
        """Creates the Research ouline on Given Topic"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=[self.essay_writer()],  # Automatically created by the @agent decorator
            tasks=[self.write_essay()],  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

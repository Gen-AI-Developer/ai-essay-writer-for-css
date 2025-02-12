#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from writer.crews.poem_crew.poem_crew import OutlineCrew, EssayCrew


class EssayState(BaseModel):
    essay_outline: str = ""
    essay: str = ""


class PoemFlow(Flow[EssayState]):

    @start()
    def generate_essay_ouline(self):
        topic = "The impact of technology on society"
        print("Generating Essay Outline")
        result = (
            OutlineCrew()
            .crew()
            .kickoff(inputs={"topic": topic})
        )
        self.state.essay_outline = result.raw
        return {"essay_outline": result.raw}

    @listen(generate_essay_ouline)
    def generate_essay(self):
        print("Generating essay")
        result = (
            EssayCrew()
            .crew()
            .kickoff(inputs={"essay_outline": self.state.essay_outline})
        )

        print("Essay generated", result.raw)
        self.state.essay = result.raw

    @listen(generate_essay)
    def save_essay(self):
        print("Saving essay")
        with open("essay.txt", "w") as f:
            f.write(self.state.essay)


def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


# def plot():
#     poem_flow = PoemFlow()
#     poem_flow.plot()


if __name__ == "__main__":
    kickoff()

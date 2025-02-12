#!/usr/bin/env python
from pydantic import BaseModel

from crewai.flow import Flow, listen, start, and_ , or_

from writer.crews.poem_crew.poem_crew import OutlineAndEssayCrew


class EssayState(BaseModel):
    topic: str = ""
    essay_outline: str = ""
    essay: str = ""


class PoemFlow(Flow[EssayState]):

    @start()
    def generate_essay_ouline(self):
        self.state.topic = input('Enter Question or Topic for the Essay:> ')
        print("Generating Essay Outline")
        result = (
            OutlineAndEssayCrew()
            .outline_crew()
            .kickoff(inputs={"topic": self.state.topic})
        )
        self.state.essay_outline = result.raw

        return {"essay_outline": result.raw}

    @listen(generate_essay_ouline)
    def generate_essay(self):
        print("Generating essay")
        result = (
            OutlineAndEssayCrew()
            .essay_crew()
            .kickoff(inputs={"essay_outline": self.state.essay_outline})
        )

        print("Essay generated", result.raw)
        self.state.essay = result.raw

    @listen(and_(generate_essay_ouline,generate_essay))
    def save_essay(self):
        print("Saving essay")
        with open(f"{self.state.topic} - Outline.md", "w") as f:
            f.write(self.state.essay_outline)
        with open(f"{self.state.topic}.md", "w") as f:
            f.write(self.state.essay)


def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()
    

def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()

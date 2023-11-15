class Question:
    """Question on a questionnaire."""

    def __init__(self, question, choices=None, allow_text=False):
        """Create question (assume Yes/No for choices."""

        if not choices:
            choices = ["Yes", "No"]

        self.question = question
        self.choices = choices
        self.allow_text = allow_text


class Survey:
    """Questionnaire."""

    def __init__(self, title, instructions, questions):
        """Create questionnaire."""

        self.title = title
        self.instructions = instructions
        self.questions = questions


satisfaction_survey = Survey(
    "Customer Satisfaction Survey",
    "Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?"),
        Question("Did someone else shop with you today?"),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?"),
    ])

personality_quiz = Survey(
    "Rithm Personality Test",
    "Learn more about yourself with our personality quiz!",
    [
        Question("Do you ever dream about code?"),
        Question("Do you ever have nightmares about code?"),
        Question("Do you prefer porcupines or hedgehogs?",
                 ["Porcupines", "Hedgehogs"]),
        Question("Which is the worst function name, and why?",
                 ["do_stuff()", "run_me()", "wtf()"],
                 allow_text=True),
    ]
)

dreams_quiz = Survey(
    "A Quiz About Your Dreams",
    "Dig deeper to uncover what your dreams may mean!",
    [
        Question("Have you ever dreamt you could fly?"),
        Question("Have you ever dreamt your teeth were falling out?"),
        Question("Have you ever dreamt you died?"),
        Question("Have you ever seen the movie 'Inception'?"),
        Question("Did the top ever fall over at the end?"),
        Question("Have you ever seen the movie 'Dreamscape'?"),
        Question("Do you ever remember your dreams?")
    ]
)

music_quiz = Survey(
    "A Survey On Your Musical Taste",
    "What kind of music do you like?",
    [
        Question("Do you like pop music?"),
        Question("Do you like classic rock?"),
        Question("Do you like hip hop?"),
        Question("Do you like jazz?"),
        Question("Do you like reggae?"),
        Question("Do you like country?"),
        Question("Do you like classical?")
    ]
)

surveys = {
    "satisfaction": satisfaction_survey,
    "personality": personality_quiz,
    "dreams": dreams_quiz,
    "music": music_quiz,
}
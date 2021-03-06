import math
import random

class Experience:
    def __init__(self, score, experience):
        self.score = score
        self.experience = experience

class ExperienceBuffer:
    def __init__(self, maxLen):
        self.maxLen = maxLen
        self.buffer = [None] * maxLen
        self.len = 0
        self.totalScore = 0
        self.avgScore = 0
        self.insertPoint = 0

    def __iadd__(self, experiences):
        '''
        Add multiple experiences, with weight
        '''
        for e in experiences:
            self.add(e, True)

    def add(self, experience, weighted=False):
        '''
        Add the experience to buffer
        experience: Experience-like object
        weighted: add multiple copies if experience's score is higher than average score in buffer
        '''
        if weighted:
            nInsert = (experience.score / self.avgScore) ** 3 if self.avgScore != 0 else 0
            nInsert = max(1, math.ceil(nInsert))
        else:
            nInsert = 1

        for i in range(nInsert):
            self._addSingleExperience(experience)

    def _addSingleExperience(self, experience):
        if not self.buffer[self.insertPoint] is None:
            self.totalScore -= self.buffer[self.insertPoint].score
        self.buffer[self.insertPoint] = experience
        self.totalScore += experience.score
        self.insertPoint = (self.insertPoint + 1) % self.maxLen
        self.len = min(self.maxLen, self.len + 1)
        self.avgScore = self.totalScore / self.len


    def sample(self, batchSize=1):
        return [self.buffer[random.randrange(self.len)] for _ in range(batchSize)]
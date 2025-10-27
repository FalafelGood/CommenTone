from typing import Dict

class VaderScores:
  def __init__(self):
    self.pos_scores = []
    self.neu_scores = []
    self.neg_scores = []
    self.weights = [] # Multiplicative weight for the score
  
  def add_score(self, score: Dict, likes: int):
    f"""score is a dict with keys ("pos", "neu", "neg") and likes is the number of times the corresponding comment has been liked"""
    self.pos_scores.append(score['pos'])
    self.neu_scores.append(score['neu'])
    self.neg_scores.append(score['neg'])
    self.weights.append(likes + 1) # Multiplicative factor

  def average_scores(self):
    avg_pos = sum(self.pos_scores) / len(self.pos_scores)
    avg_neu = sum(self.neu_scores) / len(self.neu_scores)
    avg_neg = sum(self.neg_scores) / len(self.neg_scores)
    return {"avg_pos": round(avg_pos, 3), "avg_neu": round(avg_neu, 3), "avg_neg": round(avg_neg, 3)}

  def score_variances(self):
    mu = self.average_scores()

    avg_pos = mu["avg_pos"]
    avg_neu = mu["avg_neu"]
    avg_neg = mu["avg_neg"]

    var_pos = sum((pos - avg_pos)**2 for pos in self.pos_scores) / len(self.pos_scores)
    var_neu = sum((neu - avg_neu)**2 for neu in self.neu_scores) / len(self.neu_scores)
    var_neg = sum((neg - avg_neg)**2 for neg in self.neg_scores) / len(self.neg_scores)

    return {"var_pos": round(var_pos, 3), "var_neu": round(var_neu, 3), "var_neg": round(var_neg, 3)}
  
  def weighted_average_scores(self):
    """Calculate weighted average scores using comment likes as weights"""
    
    if not self.weights or sum(self.weights) == 0:
      # If weights are not defined for some reason, return a simple average
      print("WARNING -- weights in VaderScores were improperly initialized. \"weighted_average_scores\" is defaulting to \"average_scores\"")
      return self.average_scores()
    
    total_weight = sum(self.weights)
    weighted_pos = sum(pos * weight for pos, weight in zip(self.pos_scores, self.weights)) / total_weight
    weighted_neu = sum(neu * weight for neu, weight in zip(self.neu_scores, self.weights)) / total_weight
    weighted_neg = sum(neg * weight for neg, weight in zip(self.neg_scores, self.weights)) / total_weight
    
    return {"weighted_avg_pos": round(weighted_pos, 3), 
            "weighted_avg_neu": round(weighted_neu, 3), 
            "weighted_avg_neg": round(weighted_neg, 3)}

  def kindness(self):
    weighted_average_scores = self.weighted_average_scores()
    P = weighted_average_scores['weighted_avg_pos']
    N = weighted_average_scores['weighted_avg_neg']
    return ((P-N)/(P+N))

  def volatility(self):
    weighted_average_scores = self.weighted_average_scores()
    P = weighted_average_scores['weighted_avg_pos']
    N = weighted_average_scores['weighted_avg_neg']
    Z = weighted_average_scores['weighted_avg_neu']
    return 1/(Z + abs(P-N))



if __name__ == "__main__":
    print("Running unit test for vaderscores.py")
    sample_scores = [
        {'pos': 0.8, 'neu': 0.2, 'neg': 0.0},
        {'pos': 0.0, 'neu': 0.3, 'neg': 0.7}, 
        {'pos': 0.1, 'neu': 0.7, 'neg': 0.2}       
    ]
    sample_like_counts = [5, 1, 0]
    VS = VaderScores()
    for score, like_count in zip(sample_scores, sample_like_counts):
        VS.add_score(score, like_count)

    print("VaderScore object initialized without error")
    print(f"Average scores for sample data: {VS.average_scores()}")
    print(f"Weighted average scores for sample data: {VS.weighted_average_scores()}")

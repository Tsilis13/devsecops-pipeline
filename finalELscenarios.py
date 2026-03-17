from itertools import product, combinations
from collections import defaultdict
from typing import List, Tuple, Callable, Dict, Any

# ==========================================
# 1. CORE DATA (Update only when H2H changes)
# ==========================================
# Matches the comprehensive data from genscenarios.py
head_to_head_results = {
    ('asm', 'bay'): (1, 1, 18), 
    ('asm', 'efes'): (2, 0, 31),
    ('asm', 'barca'): (0, 2, -29),
    ('asm', 'rma'): (1, 1, -18),
    ('asm', 'cvz'): (0, 2, -14),
    ('bay', 'efes'): (0, 2, -16),
    ('bay', 'barca'): (2, 0, 23),
    ('bay', 'rma'): (1, 1, -4),
    ('bay', 'cvz'): (1, 1, -6),
    ('bay', 'pbb'): (1, 1, -3),
    ('efes', 'barca'): (0, 2, -19),
    ('efes', 'rma'): (2, 0, 16),
    ('efes', 'cvz'): (2, 0, 22),
    ('efes', 'pbb'): (0, 2, -13),
    ('efes', 'ea'): (2, 0, 56),
    ('barca', 'rma'): (0, 2, -5),
    ('barca', 'cvz'): (1, 1, -4),
    ('barca', 'pbb'): (1, 1, -5),
    ('rma', 'cvz'): (2, 0, 29),
    ('rma', 'pbb'): (2, 0, 12),
    ('cvz', 'pbb'): (2, 0, 19),
    ('pbb', 'ea'): (1, 1, -8),
    ('ea', 'par'): (1, 1, -3),
    ('ea', 'zal'): (1, 1, -2),
    ('par', 'zal'): (1, 1, 2),
    ('zal', 'bkn'): (0, 2, -8),
    ('zal', 'asvel'): (0, 2, -15),
    ('bkn', 'asvel'): (1, 1, 29),
    ('oly', 'pao'): (2, 0, 7),
    ('oly', 'fener'): (0, 2, -21),
    ('fener', 'pao'): (0, 2, -6),
    ('pao', 'asm'): (1, 1, 9),
    ('bkn', 'par'): (1, 1, -7)
}

# ==========================================
# 2. SIMULATION ENGINE (Do not edit this part)
# ==========================================
def resolve_tie(teams):
    insideWins = defaultdict(int)
    insideDiff = defaultdict(int)
    for t1, t2 in combinations(teams, 2):
        if (t1, t2) in head_to_head_results:
            t1_wins, t2_wins, diff = head_to_head_results[(t1, t2)]
            insideWins[t1] += t1_wins
            insideWins[t2] += t2_wins
            if diff > 0:
                insideDiff[t1] += diff
                insideDiff[t2] -= diff
            else:
                insideDiff[t1] -= diff
                insideDiff[t2] += diff
        elif (t2, t1) in head_to_head_results:
            t2_wins, t1_wins, diff = head_to_head_results[(t2, t1)]
            insideWins[t1] += t1_wins
            insideWins[t2] += t2_wins
            if diff > 0:
                insideDiff[t2] += diff
                insideDiff[t1] -= diff
            else:
                insideDiff[t2] -= diff
                insideDiff[t1] += diff

    sorted_teams_by_wins = sorted(teams, key=lambda team: (-insideWins[team], team))

    if all(insideWins[team] == insideWins[sorted_teams_by_wins[0]] for team in sorted_teams_by_wins):
        sorted_teams_by_wins = sorted(sorted_teams_by_wins, key=lambda team: (-insideDiff[team], team))

    return sorted_teams_by_wins

def compute_scenario_probabilities(events: List[Tuple[str, float]], outcome_function: Callable) -> Dict[Any, float]:
    n = len(events)
    outcomes = defaultdict(float)

    for scenario in product([0, 1], repeat=n):
        prob = 1.0
        for i, outcome in enumerate(scenario):
            p = events[i][1]
            prob *= p if outcome else (1 - p)
        
        result = outcome_function(scenario)
        outcomes[result] += prob

    return dict(outcomes)

# ==========================================
# 3. WEEKLY CONFIGURATION (Edit this part each week!)
# ==========================================

# A. Define the upcoming matches and the probability of the event happening (e.g., Team 1 winning)
events = [
    ("Bay vs Fener 1", 0.4538),
    ("Bay vs Fener 2", 0.5462),
    ("asvel vs Asm 2", 0.7096),
    ("asvel vs Asm 1", 0.2904),
    ("EA7 vs Bkn 1", 0.6096),
    ("EA7 vs Bkn 2", 0.3904),
    ("Par vs rma 2", 0.6635),
    ("Par vs rma 1", 0.3365),
    ("Pbb vs Ber 1", 0.8346),
    ("Efes vs Zal 1", 0.8027),
    ("Efes vs Zal 2", 0.1973),
    ("pao vs Cvz 2", 0.2412),
    ("pao vs Cvz 1", 0.7588),
    ("Barca vs Vir 1", 0.8741),
    ("Oly vs Mta 1", 0.8590),
]

# B. Define how the scenario impacts the standings
def current_week_outcome(scenario):
    # Unpack the scenario tuple in the EXACT same order as your 'events' list above
    bavfe1, bavfe2, asvas2, asvas1, eavbk1, eavbk2, pavrm2, pavrm1, pbbvber1, efvza1, efvza2, paovcvz2, paovcvz1, barvvir1, olvmta1 = scenario 
    
    wins = {
        "oly": 23 + olvmta1,
        "fener": 22 + bavfe2,
        "pao": 21 + paovcvz1,
        "asm": 20 + asvas2,
        "bay": 19 + bavfe1,
        "rma": 19 + pavrm2,
        "barca": 19 + barvvir1,
        "efes": 19 + efvza1,
        "cvz": 18 + paovcvz2,
        "pbb": 18 + pbbvber1,
        "ea": 16 + eavbk1,
        "par": 16 + pavrm1,
        "zal": 15 + efvza2,
        "bkn": 14 + eavbk2,
        "asvel": 13 + asvas1,
        "mta": 11,
        "vir": 9,
        "alba": 5
    }

    sorted_teams = sorted(wins.items(), key=lambda x: (-x[1], x[0]))
    grouped_teams = defaultdict(list)
    for team, w in sorted_teams:
        grouped_teams[w].append(team)
    
    final_ranking = []
    for win_record, teams in grouped_teams.items():
        if len(teams) > 1:
            resolved_teams = resolve_tie(teams)
            final_ranking.extend(resolved_teams)
        else:
            final_ranking.append(teams[0])

    return tuple(final_ranking)

# ==========================================
# 4. ANALYSIS & OUTPUT (Run the numbers)
# ==========================================
if __name__ == "__main__":
    print("Simulating scenarios... Please wait.")
    results = compute_scenario_probabilities(events, current_week_outcome)
    
    print("\n--- PROBABILITIES FOR TOP POSITIONS ---")
    # This checks the probability of each team landing in Positions 1 through 6
    for pos in range(6):  # Change 6 to 18 if you want to print all positions
        print(f"\nPosition {pos + 1}:")
        pos_probs = defaultdict(float)
        for ranking, prob in results.items():
            pos_probs[ranking[pos]] += prob
            
        # Print teams with > 0.1% chance for this position
        for team, total_prob in sorted(pos_probs.items(), key=lambda x: -x[1]):
            if total_prob > 0.001: 
                print(f"  {team}: {total_prob*100:.2f}%")

    print("\n--- SPECIFIC SCENARIO CHECKS ---")
    
    # Example 1: Probability of Monaco (asm) 1st AND Barca 2nd (Replaces your analysis.py logic)
    specific_prob = sum(prob for ranking, prob in results.items() if ranking[0] == 'asm' and ranking[1] == 'barca')
    print(f"Total Probability of ASM 1st and Barca 2nd: {specific_prob*100:.2f}%\n")

    # Example 2: Conditional Probability (e.g., Who finishes 6th IF Pao is 3rd?)
    target_pao_pos = 2 # 0-indexed, so 2 is 3rd place
    sixth_place_if_pao_3rd = defaultdict(float)
    total_pao_3rd_prob = sum(prob for ranking, prob in results.items() if ranking[target_pao_pos] == 'pao')

    if total_pao_3rd_prob > 0:
        for ranking, prob in results.items():
            if ranking[target_pao_pos] == 'pao':
                sixth_place_if_pao_3rd[ranking[5]] += prob # index 5 is 6th place

        print("If Pao finishes 3rd, the probabilities for 6th place are:")
        for team, raw_prob in sorted(sixth_place_if_pao_3rd.items(), key=lambda x: -x[1]):
            cond_prob = (raw_prob / total_pao_3rd_prob) * 100
            print(f"  {team}: {cond_prob:.2f}%")

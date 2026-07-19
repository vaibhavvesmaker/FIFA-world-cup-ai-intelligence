const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export type Team = {
  id: string | null;
  name: string | null;
};

export type MatchSource = {
  provider: string;
  verified: boolean;
  url?: string;
};

export type WorldCupMatch = {
  match_id: string;
  kickoff: string | null;
  status: "scheduled" | "finished";
  stage: string | null;
  group: string | null;
  matchday: string | null;
  stadium_id: string | null;
  home_team: Team;
  away_team: Team;
  score: {
    home: number | null;
    away: number | null;
  };
  source: MatchSource;
};

type WorldCupMatchesResponse = {
  count: number;
  source: MatchSource;
  matches: WorldCupMatch[];
};

export async function getWorldCup2026Matches(): Promise<WorldCupMatchesResponse> {
  const response = await fetch(`${API_BASE_URL}/matches/2026`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`World Cup API returned ${response.status}`);
  }

  return response.json();
}
export type MatchPrediction = {
    match_id: string;
    teams: {
      home: Team;
      away: Team;
    };
    probabilities: {
      home_win: number;
      draw: number;
      away_win: number;
    };
    ratings: {
      home: number;
      away: number;
    };
    model: {
      name: string;
      version: string;
      training_matches: number;
      generated_at: string;
    };
    data: {
      provider: string;
      verified: boolean;
      leakage_guard: string;
    };
  };
  
  export async function getMatchPrediction(
    matchId: string,
  ): Promise<MatchPrediction> {
    const response = await fetch(`${API_BASE_URL}/predictions/${matchId}`, {
      cache: "no-store",
    });
  
    if (!response.ok) {
      throw new Error(`Prediction API returned ${response.status}`);
    }
  
    return response.json();
  }
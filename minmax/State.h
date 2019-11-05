//
// Created by stephen on 10/18/19.
//

#ifndef UNTITLED_STATE_H
#define UNTITLED_STATE_H

#include <string>
#include <vector>

using namespace std;


class State
{
    private:
        vector<vector<string> > hands;
        int owningPlayer;
        int player;
        string leadCard;
        int leadingPlayer;
        vector<string> trick;
        vector<int> points;
        int numTricks;
        vector<string> cardsPlayed;
        string restriction;
        string bid;
        int findWinningCard();
        vector<int> findSuit(char suit, int defaultVal = -1);
        void findWinningPlayer();

    public:
        State();
        State(vector<vector<string>> hands, int player, string leadCard, int leadingPlayer, vector<string> trick, vector<int> points,
          int numTricks, vector<string> cardsPlayed, string restriction = "asc", string bid = "");
        vector<string> getHand(int hand);
        vector<vector<string>> getHands();
        void setPlayer(int player);
        int getPlayer();
        void setLeadCard(string card);
        string getLeadCard();
        void setLeadingPlayer(int leadingPlayer);
        int getLeadingPLayer();
        vector<string> getTrick();
        vector<int> getPoints();
        void setNumTricks(int numTricks);
        int getNumTricks();
        vector<string> getCardsPlayed();
        void setRestriction(string restriction);
        string getRestriction();
        void setBid (string bid);
        string getBid();

        void removeFromHand(int hand, int position);
        void addToHand(int hand, string card, int position);
        void addToCardsPlayed(string card);
        void removeFromCardsPlayed();
        void addToTrick(string card);
        void removeFromTrick();
        void testTrick();
        bool handsAreEmpty();
        int evalTricks();
        void printHands();
        bool operator==(State state);
        State copy();

};


#endif //UNTITLED_STATE_H

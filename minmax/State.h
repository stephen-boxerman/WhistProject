//
// Created by stephen on 10/18/19.
//

#ifndef UNTITLED_STATE_H
#define UNTITLED_STATE_H

#include <string>
#include <list>
#include <array>
#include <unordered_set>

using namespace std;


class State
{
    private:
        unordered_set<string> hands[4];
        unordered_set<string> cardsPlayed;
        list<unsigned long long> hash;
        list<string> trick;
        string restriction;
        string bid;
        string leadCard;
        int points[2];
        int owningPlayer;
        int player;
        int leadingPlayer;
        int numTricks;
        int findWinningCard();
        list<int> findSuit(char suit, int defaultVal = -1);
        void findWinningPlayer();

    public:
        State();
        ~State();
        State(unordered_set<string> (&hands)[4], int player, string leadCard, int leadingPlayer, list<string> &trick, int (&points)[2],
                 int numTricks, list<string> &cardsPlayed, string restriction = "acs", string bid = "p");
        unordered_set<string> getHand(int hand);
        void setPlayer(int player);
        int getPlayer();
        void setLeadCard(string card);
        string getLeadCard();
        unordered_set<string> * getCardsPlayed();
        void setRestriction(string res);
        void setBid(string bid);
        int * getPoints();
        void setPoints(int (&points)[2]);

        void removeFromHand(int hand, string card);
        void addToHand(int hand, string card);
        void addToCardsPlayed(string card);
        void removeFromCardsPlayed(string card);
        void addToTrick(string card);
        void removeFromTrick();
        void testTrick();
        bool handsAreEmpty();
        int evalTricks();
        void createHash();
        list<unsigned long long> * getHash();
        State * copy();

};


#endif //UNTITLED_STATE_H

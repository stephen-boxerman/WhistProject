//
// Created by stephen on 10/18/19.
//

#ifndef UNTITLED_STATE_H
#define UNTITLED_STATE_H

#include <string>
#include <list>
#include <array>

using namespace std;


class State
{
    private:
        list<string> hands[4];
        int owningPlayer;
        int player;
        string leadCard;
        int leadingPlayer;
        list<string> trick;
        int points[2];
        int numTricks;
        list<string> cardsPlayed;
        string restriction;
        string bid;
        int findWinningCard();
        int[4] findSuit(char suit, int defaultVal = -1);
        void findWinningPlayer();
        unsigned long hash[5];
        void setOwningPlayer(int owningPlayer);

    public:
        State();
        ~State();
        State(list<string> hands[4], int player, string leadCard, int leadingPlayer, list<string> trick, int points[2],
          int numTricks, list<string> cardsPlayed, string restriction = "asc", string bid = "");
        list<string> getHand(int hand);
        void setPlayer(int player);
        int getPlayer();
        void setLeadCard(string card);
        string getLeadCard();
        list<string> getCardsPlayed();

        void removeFromHand(int hand, string card);
        void addToHand(int hand, string card);
        void addToCardsPlayed(string card);
        void removeFromCardsPlayed();
        void addToTrick(string card);
        void removeFromTrick();
        void testTrick();
        bool handsAreEmpty();
        int evalTricks();
        void createHash();
        unsigned long * getHash();
        State copy();

};


#endif //UNTITLED_STATE_H

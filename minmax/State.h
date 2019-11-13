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
        list<int> findSuit(char suit, int defaultVal = -1);
        void findWinningPlayer();
        list<unsigned long long> hash;
        void setOwningPlayer(int owningPlayer);

    public:
        State();
        ~State();
        State(list<string> (&hands)[4], int player, string leadCard, int leadingPlayer, list<string> &trick, int (&points)[2],
                 int numTricks, list<string> &cardsPlayed, string restriction = "acs", string bid = "p");
        list<string> getHand(int hand);
        void setPlayer(int player);
        int getPlayer();
        void setLeadCard(string card);
        string getLeadCard();
        list<string> * getCardsPlayed();

        void removeFromHand(int hand, string card);
        void addToHand(int hand, string card, int pos);
        void addToCardsPlayed(string card);
        void removeFromCardsPlayed();
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

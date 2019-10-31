#include <iostream>
#include <string.h>
#include "State.h"
#include <ctime>
#include <vector>
#include <algorithm>
#include <bits/stdc++.h>


using namespace std;

template < typename type>
bool findInVector(const std::vector<type>  & vecOfElements, const type & element)
{
    bool result;

    // Find given element in vector
    auto it = std::find(vecOfElements.begin(), vecOfElements.end(), element);

    if (it != vecOfElements.end())
    {
        result = true;
    }
    else
    {
        result = false;
    }

    return result;
}

int nextPLayer(int player) {return (player + 1) % 4;}

int suitInHand(char suit, vector<string> hand)
{
    int numSuit = 0;
    vector<string>::iterator it;

    for(it = hand.begin(); it < hand.end(); it++)
    {
        string card = *it;
        if(card[0] == suit)
        {
            numSuit++;
        }
    }

    return numSuit;
}

bool isLeagal(State state, string card, vector<string> hand)
{
    string leadCard = state.getLeadCard();

    if(card == "") return false;
    else if(leadCard.empty()) return true;
    else if(suitInHand(leadCard[0], hand) == 0) return true;
    else if(not findInVector(hand, card)) return false;
    else if(findInVector(state.getCardsPlayed(), card)) return false;
    else if(card[0] != leadCard[0]) return false;
    else return true;
}

int minmax(int alpha, int beta, State state)
{
    bool isMax;
    int bestVal;
    int index = -1;

    state.setPlayer(nextPLayer(state.getPlayer()));

    state.testTrick();

    int player = state.getPlayer();

    isMax = (player == 0 or player == 2);

    if(isMax)
    {
        bestVal = numeric_limits<int>::min();
    }
    else
    {
        bestVal = numeric_limits<int>::max();
    }

    if(state.handsAreEmpty())
    {
        int score = state.evalTricks();
        return score;
    }

    vector<string> cards = state.getHand(player);

    if(state.getLeadCard() == "")
    {
        vector<string> hand = state.getHand(player);

        for(vector<string>::iterator it = hand.begin(); it<hand.end(); it++)
        {
            if(*it != "")
            {
                string card = *it;
                state.addToCardsPlayed(card);
                state.addToTrick(card);
                state.setLeadCard(card);
                state.removeFromHand(player, card);
                bestVal = minmax(alpha, beta, state.copy());
                break;
            }
        }
    }

    else
    {
        for (vector<string>::iterator it = cards.begin(); it < cards.end(); it++) {
            string card = *it;
            int pos;

            if (isLeagal(state, card, cards)) {

                pos = (int)distance(cards.begin(), it);
                state.addToCardsPlayed(card);
                state.addToTrick(card);
                state.removeFromHand(player, card);
                int value = minmax(alpha, beta, state.copy());
                state.addToHand(player, card, pos);
                state.removeFromTrick();
                state.removeFromCardsPlayed();

                if (isMax) {
                    if (value > beta) {
                        bestVal = value;
                        break;
                    } else if (value > bestVal) {
                        bestVal = value;
                        alpha = value;
                    }
                } else {
                    if (value < alpha) {
                        bestVal = value;
                        break;
                    } else if (value < bestVal) {
                        bestVal = value;
                        beta = value;
                    }
                }


            }
        }
    }

    return bestVal;

}


string getOptimalCard(State state)
{
    int alpha = numeric_limits<int>::min();
    int beta = numeric_limits<int>::max();
    int bestVal = numeric_limits<int>::min();
    string optCard;
    int value;

    int player = state.getPlayer();
    vector<string> hand = state.getHand(player);
    vector<string>::iterator it;

    for(it = hand.begin(); it < hand.end(); it++)
    {
        int pos;
        if(isLeagal(state, *it, hand))
        {
            string card = *it;
            cout<<card<<endl;
            pos = (int)distance(hand.begin(), it);
            state.addToCardsPlayed(card);
            state.addToTrick(card);
            state.removeFromHand(player, card);
            value = minmax(alpha, beta, state.copy());
            state.addToHand(player, card, pos);
            state.removeFromCardsPlayed();
            state.removeFromTrick();

            cout<<"Card -> "<<card<<", Value -> "<<value<<endl;

            if(value > bestVal)
            {
                bestVal = value;
                alpha = value;
                optCard = card;
            }
        }
    }

    return optCard;
}

void printDeck(vector<string> deck)
{
    for(vector<string>::iterator it = deck.begin(); it < deck.end(); it++)
    {
        cout<<*it<<" ";
    }
}

int main()
{
    vector<string> deck;
    vector<vector<string>> hands = {{}, {}, {}, {}};

    const vector<string> SUITS = {"h", "s", "d", "c"};
    const vector<string> CARD_VALUES = {"2", "5", "8", "J", "A"};
    string card;
    const int MAX_HAND_SIZE = 5;

    deck = {"the deck"};

    hands = {{"sA", "d2", "cA", "c2", "s2"}, {"d5", "hJ", "h5", "h2", "c5"}, {"dJ", "dA", "d8", "sJ", "s8"}, {"s5", "h8", "sJ", "c8", "hA"}};

//    for(auto suit = SUITS.begin(); suit < SUITS.end(); suit++)
//    {
//
//        for (auto value = CARD_VALUES.begin(); value < CARD_VALUES.end(); value++)
//        {
//            card = *suit;
//            card.operator+=(*value);
//            deck.emplace_back(card);
//        }
//    }
//
//    srand(time(NULL));
//    random_shuffle(deck.begin(), deck.end());
//
//    vector<string>::iterator cards = deck.begin();
//
//    for (auto i = 0; i < MAX_HAND_SIZE; i++)
//    {
//        for (auto hand = hands.begin(); hand < hands.end(); hand++)
//        {
//            vector<string>::iterator endOfHand = hand->end();
//            hand->emplace(endOfHand, *cards);
//            if(cards != deck.end()) cards++;
//        }
//    }
    string leadCard = hands[3].at(0);

    State state = State(hands, 0 ,hands[3].at(0), 3, {hands[3].at(0)}, {0,0}, 0, {hands[3].at(0)});

    state.removeFromHand(3, hands[3][0]);

   string optCard = getOptimalCard(state);

   cout<<optCard<<endl<<"Hands -> ";
   state.printHands();
   cout<<"Deck -> ";
   printDeck(deck);



    return 0;
}
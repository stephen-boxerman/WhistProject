#include <iostream>
#include <string.h>
#include "State.h"
#include <ctime>
#include <vector>
#include <algorithm>
#include <bits/stdc++.h>


using namespace std;

unordered_map<unsigned long[5], int> state_table;

template < typename type>
bool findInList(const list<type>  &listOfElements, const type & element)
{
    bool result;

    // Find given element in vector
    auto it = std::find(listOfElements.begin(), listOfElements.end(), element);

    if (it != listOfElements.end())
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

int suitInHand(char suit, list<string> hand)
{
    int numSuit = 0;
    for(auto it = hand.begin(); it != hand.end(); it++)
    {
        string card = *it;
        if(card[0] == suit)
        {
            numSuit++;
        }
    }

    return numSuit;
}

bool isLeagal(State state, string card, list<string> hand)
{
    string leadCard = state.getLeadCard();

    if(card == "") return false;
    else if(leadCard.empty()) return true;
    else if(suitInHand(leadCard[0], hand) == 0) return true;
    else if(not findInList(hand, card)) return false;
    else if(findInList(state.getCardsPlayed(), card)) return false;
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
    if(not state_table.empty())
    {
       if(state_table.find(state.getHash()) != state_table.end())
       {
           return state_table[state.getHash()]
       }
    }

    list<string> cards = state.getHand(player);

    if(state.getLeadCard() == "")
    {
        list<string> hand = state.getHand(player);

        for(list<string>::iterator it = hand.begin(); it != hand.end(); it++)
        {
            int pos;
            if(*it != "")
            {
                pos = (int)distance(hand.begin(), it);
                string card = *it;
                state.addToCardsPlayed(card);
                state.addToTrick(card);
                state.setLeadCard(card);
                state.removeFromHand(player, pos);
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
                state.removeFromHand(player, pos);
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
    if(state.getCardsPlayed().size() > 8)
    {
        states.emplace_back(state.getHash());
        values.emplace_back(bestVal);
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

    cout<<state.getLeadCard()<<endl;
    for(auto card = hand.begin(); card < hand.end(); card++)
    {
        cout<<*card<<" ";
    }

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
            state.removeFromHand(player, pos);
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
    const vector<string> CARD_VALUES = {"2", "3", "4", "5", "6", "7", "8", "9", "t", "J", "Q", "K", "A"};

    string card;
    const int MAX_HAND_SIZE = 13;

    for(auto suit = SUITS.begin(); suit < SUITS.end(); suit++)
    {
        for (auto val = CARD_VALUES.begin(); val < CARD_VALUES.end(); val++)
        {
            card = *suit + *val;
            deck.emplace_back(card);
        }
    }


    srand(time(NULL));
    random_shuffle(deck.begin(), deck.end());

    vector<string>::iterator cards = deck.begin();

    for (auto i = 0; i < MAX_HAND_SIZE; i++)
    {
        for (auto hand = hands.begin(); hand < hands.end(); hand++)
        {
            vector<string>::iterator endOfHand = hand->end();
            hand->emplace(endOfHand, *cards);
            if(cards != deck.end()) cards++;
        }
    }
    string leadCard = hands[3].at(0);

    State state = State(hands, 0 ,hands[3].at(0), 3, {hands[3].at(0)}, {0,0}, 0, {hands[3].at(0)});
    state.createHash();

    state.removeFromHand(3, 0);

   string optCard = getOptimalCard(state);

   cout<<"Optimal Card -> "<<optCard<<endl;



    return 0;
}
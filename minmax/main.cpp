#include <iostream>
#include <string.h>
#include "State.h"
#include <ctime>
#include <vector>
#include <algorithm>
#include <bits/stdc++.h>
#include <functional>


using namespace std;
unsigned long long hash_combine(size_t &seed, unsigned long long item)
{
    return (seed + item) * (size_t)29;
}

struct key
{
    unsigned long long hand1, hand2, hand3, hand4, stateInfo;
    key(list<unsigned long long> (&state_hash))
    {
        auto it = state_hash.begin();
        this->hand1 = *it;
        advance(it, 1);
        this->hand2 = *it;
        advance(it, 1);
        this->hand3 = *it;
        advance(it, 1);
        this->hand4 = *it;
        advance(it, 1);
        this->stateInfo = *it;
    }

    bool operator==(key const& Key) const
    {
        if(this->hand1 != Key.hand1)
        {
            return false;
        }

        if(this->hand2 != Key.hand2)
        {
            return false;
        }

        if(this->hand3 != Key.hand3)
        {
            return false;
        }

        if(this->hand4 != Key.hand4)
        {
            return false;
        }

        if(this->stateInfo != Key.stateInfo)
        {
            return false;
        }

        return true;
    }
};

struct hash_key
{
    size_t operator()(key const& Key) const
    {
        std::hash<unsigned long long> long_hash;

        size_t seed = 0;
        seed += hash_combine(seed, Key.hand1);
        seed += hash_combine(seed, Key.hand2);
        seed += hash_combine(seed, Key.hand3);
        seed += hash_combine(seed, Key.hand4);
        seed += hash_combine(seed, Key.stateInfo);
        return seed;

    }

};

unordered_map<key, int, hash_key> state_table;



template <typename type>

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

int suitInHand(char suit, unordered_set<string> hand)
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

bool isLeagal(State * state, string card, int hand)
{
    string leadCard = state->getLeadCard();

    if(card == "") return false;
    else if(leadCard.empty()) return true;
    else if(suitInHand(leadCard[0], state->getHand(hand)) == 0) return true;
    else if(state->getCardsPlayed()->find(card) != state->getCardsPlayed()->end()) return false;
    else if(card[0] != leadCard[0]) return false;
    else return true;
}

int minmax(int alpha, int beta, State * state) {
    bool isMax;
    int bestVal;
    int index = -1;
    list<unsigned long long> *hash = state->getHash();
    struct key Key = key(*hash);

    state->setPlayer(nextPLayer(state->getPlayer()));

    state->testTrick();

    int player = state->getPlayer();

    isMax = (player == 0 or player == 2);

    if (isMax) {
        bestVal = numeric_limits<int>::min();
    } else {
        bestVal = numeric_limits<int>::max();
    }

    if (state->handsAreEmpty()) {
        int score = state->evalTricks();
        return score;
    }
    if(not state_table.empty())
    {
        if(state_table.count(Key) != 0)
        {
            return state_table[Key];
        }
    }

    unordered_set<string> cards = state->getHand(player);

    if(state->getLeadCard() == "")
    {
        string card = *(state->getHand(player).begin());
        state->addToCardsPlayed(card);
        state->addToTrick(card);
        state->setLeadCard(card);
        state->removeFromHand(player, card);
        bestVal = minmax(alpha, beta, state);
    }

    else
    {
        for (auto it = cards.begin(); it != cards.end(); it++) {
            string card = *it;
            int pos;

            if (isLeagal(state, card, player)) {
                state->addToCardsPlayed(card);
                state->addToTrick(card);
                state->removeFromHand(player, card);
                int value = minmax(alpha, beta, state);
                state->setPlayer(player);
                state->addToHand(player, card);
                state->removeFromTrick();
                state->removeFromCardsPlayed(card);
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

    if(state->getCardsPlayed()->size() >26)
        state_table[Key] = bestVal;
    return bestVal;

}




string getOptimalCard(State * state)
{
    int alpha = numeric_limits<int>::min();
    int beta = numeric_limits<int>::max();
    int bestVal = numeric_limits<int>::min();
    string optCard;
    int value;

    int player = state->getPlayer();
    unordered_set<string> hand = state->getHand(player);
    vector<string>::iterator it;

    for(auto it = hand.begin(); it != hand.end(); it++)
    {
        int pos;
        string card = *it;
        if(isLeagal(state, card, player))
        {
            string card = *it;
            cout<<card<<endl;
            pos = (int)distance(hand.begin(), it);
            state->addToCardsPlayed(card);
            state->addToTrick(card);
            state->removeFromHand(player, card);
            value = minmax(alpha, beta, state->copy());
            state->addToHand(player, card);
            state->removeFromCardsPlayed(card);
            state->removeFromTrick();

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

string getOptimalBid(State * state)
{
    const list<string> TRUMP = {"h", "s", "d", "c"};
    const list<string> NO_TRUMP = {"asc", "desc"};
    const list<string> BIDS = {"p", "1", "1no", "2", "2no", "3", "3no",
                               "4", "4no", "5", "5no", "6", "6no", "7", "7no"};

    int alpha = numeric_limits<int>::min();
    int beta = numeric_limits<int>::max();

    int bestVal = alpha;

    int value;
    string optBid;

    for(auto bid = BIDS.begin(); bid != BIDS.end(); bid++)
    {
        state -> setBid(*bid);

        cout<<(*bid)<<endl;

        if(*bid == "p")
        {
            value = minmax(alpha, beta, state->copy());
        }

        else if(distance(BIDS.begin(), bid) % 2 == 0)
        {
            for(auto res = NO_TRUMP.begin(); res != NO_TRUMP.end(); res++)
            {
                state->setRestriction(*res);
                value = minmax(alpha, beta, state->copy());

            }
        }
        else
        {
            for(auto trump = TRUMP.begin(); trump != TRUMP.end(); trump++)
            {
                state->setRestriction(*trump);
                value = minmax(alpha, beta, state->copy());
            }
        }

        if(value > bestVal)
        {
            bestVal = value;
            optBid = *bid;
        }

    }

    return optBid;

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
    unordered_set<string> hands[4] = {{}, {}, {}, {}};

    const vector<string> SUITS = {"h", "s", "d", "c"};
    const vector<string> CARD_VALUES = {"2", "3", "4", "5", "6", "7", "8", "9", "t", "J", "Q", "K", "A"};

    string card;
    const int MAX_HAND_SIZE = CARD_VALUES.size();

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
        for (int i = 0; i < 4; i++)
        {
            hands[i].insert(*cards);
            if(cards != deck.end()) cards++;
        }
    }

//    State::State(list<string> (&hands)[4], int player, string leadCard, int leadingPlayer, list<string> &trick, int points[2],
//        int numTricks, list<string> &cardsPlayed, string restriction, string bid)

    string leadCard = *(hands[3].begin());
    list<string> trick;
    list<string> cardsPlayed;
    int points[2] = {0,0};

    trick.push_back(leadCard);
    cardsPlayed.push_back(leadCard);

    State * state = new State(hands, 0 , leadCard, 3, trick, points, 0, cardsPlayed);

    state->removeFromHand(3, leadCard);

    state->createHash();

   string optCard = getOptimalCard(state);

   cout<<"Optimal Card -> "<<optCard<<endl;

//    string optBid = getOptimalBid(state);
//
//    cout<<optBid<<endl;



    return 0;
}
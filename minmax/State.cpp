//
// Created by stephen on 10/18/19.
//

#include <iostream>
#include "State.h"
#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include <fstream>

using namespace std;

map<char, int> CARD_VALUES = {{'2', 2}, {'3', 3}, {'4', 4}, {'5', 5}, {'6', 6}, {'7', 7}, {'8', 8}, {'9', 9},
                                      {'t', 10}, {'J', 11}, {'Q', 12}, {'K', 13}, {'A', 14}};

const map<string, int> POSSIBLE_BIDS = {{"p", 0}, {"1", 1}, {"1no", 2}, {"2", 3}, {"2no", 4}, {"3", 5}, {"3no", 6},
                                       {"4", 7}, {"4no", 8}, {"5", 9}, {"5no", 10}, {"6", 11}, {"6no", 12}, {"7", 13},
                                       {"7no", 14}};

const vector<string> DECK = {"h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "ht", "hJ", "hQ", "hK", "hA", "s2", "s3",
                             "s4", "s5", "s6", "s7", "s8", "s9", "st", "sJ", "sQ", "sK", "sA", "d2", "d3", "d4", "d5",
                             "d6", "d7", "d8", "d9", "dt", "dJ", "dQ", "dK", "dA", "c2", "c3", "c4", "c5", "c6", "c7",
                             "c8", "c9", "ct", "cJ", "cQ", "cK", "cA"};

const map<string, unsigned long> DECK_MAP = {{"h2", 1}, {"h3", 2}, {"h4", 4}, {"h5", 8},
                                             {"h6", 16}, {"h7", 32}, {"h8", 64}, {"h9", 128},
                                             {"ht", 256}, {"hJ", 512}, {"hQ", 1024}, {"hK", 2048},
                                             {"hA", 4096}, {"s2", 8192}, {"s3", 16384},
                                             {"s4", 32768}, {"s5", 65536}, {"s6", 131072},
                                             {"s7", 262144}, {"s8", 524288}, {"s9", 1048576},
                                             {"st", 2097152}, {"sJ", 4194304}, {"sQ", 8388608},
                                             {"sK", 16777216}, {"sA", 33554432}, {"d2", 67108864},
                                             {"d3", 134217728}, {"d4", 268435456}, {"d5", 536870912},
                                             {"d6", 1073741824}, {"d7", 2147483648}, {"d8", 4294967296},
                                             {"d9", 8589934592}, {"dt", 17179869184}, {"dJ", 34359738368},
                                             {"dQ", 68719476736}, {"dK", 137438953472}, {"dA", 274877906944},
                                             {"c2", 549755813888}, {"c3", 1099511627776}, {"c4", 2199023255552},
                                             {"c5", 4398046511104}, {"c6", 8796093022208}, {"c7", 17592186044416},
                                             {"c8", 35184372088832}, {"c9", 70368744177664}, {"ct", 140737488355328},
                                             {"cJ", 281474976710656}, {"cQ", 562949953421312}, {"cK", 1125899906842624},
                                             {"cA", 2251799813685248}};

template < typename type>
int findInVector(const vector<type>  & vecOfElements, const type & element)
{
    int result;

    // Find given element in vector
    auto it = std::find(vecOfElements.begin(), vecOfElements.end(), element);

    if (it != vecOfElements.end())
    {
        result = (int) distance(vecOfElements.begin(), it);
    }
    else
    {
        result = -1;
    }

    return result;
}

template < typename type>
int findInList(const list<type>  & listOfElements, const type & element)
{
    int result;

    // Find given element in vector
    auto it = std::find(listOfElements.begin(), listOfElements.end(), element);

    if (it != listOfElements.end())
    {
        result = (int) distance(listOfElements.begin(), it);
    }
    else
    {
        result = -1;
    }

    return result;
}

State::State() {};

State::State(list<string> hands[4], int player, string leadCard, int leadingPlayer, list<string> trick, int points[2],
        int numTricks, list<string> cardsPlayed, string restriction, string bid)
{
    this->player = player;
    this->owningPlayer = this->player;
    this->leadCard = leadCard;
    this->leadingPlayer = leadingPlayer;
    this->numTricks = numTricks;
    this->restriction = restriction;
    this->bid = bid;

    this->hands[0] = hands[0];
    this->hands[1] = hands[1];
    this->hands[2] = hands[2];
    this->hands[3] = hands[3];
    this->trick.operator=(trick);
    this->cardsPlayed.operator=(cardsPlayed);
    this->points[0] = points[0];
    this->points[1] = points[1];
}

State::~State()
{

}

list<string> State::getHand(int hand) {return this->hands[hand];}

void State::setPlayer(int player) {this->player = player;}

int State::getPlayer() {return this->player;}

void State::setLeadCard(string card) {this->leadCard = card;}

string State::getLeadCard() {return this->leadCard;}



void State::removeFromHand(int hand, string card)
{
   this -> hands[hand].remove(card);
}

void State::addToHand(int hand, string card)
{
    this->hands[hand].emplace_back(card);
    //hands[hand].emplace(hands[hand].begin() + position, card);
}

void State::addToCardsPlayed(string card) {this -> cardsPlayed.emplace_back(card);}

void State::addToTrick(string card) {this -> trick.emplace_back(card);}

void State::removeFromCardsPlayed() {this->cardsPlayed.pop_back();}

void State::removeFromTrick() {this -> trick.pop_back();}

list<int> State::findSuit(char suit, int defaultVal)
{
    list<int> card_vals;
    for(auto it = this->trick.begin(); it != this->trick.end(); it++)
    {
        string card = *it;
        if(card[0] == suit)
        {
            char cardVal = card[1];
            int value = CARD_VALUES.at(cardVal);
            card_vals.emplace_back(value);
        }
        else card_vals.emplace_back(defaultVal);
    }

    return card_vals;

}

int State::findWinningCard()
{
    list<int> values;
    list<int>::iterator winningCard;

    if(this -> restriction == "asc")
    {
        values = this -> findSuit(this->leadCard[0]);
    }
    else if(this -> restriction == "desc")
    {
        values = this->findSuit(this->leadCard[0], 30);
    }
    else
    {
        char cRestriction = this->restriction[0];
        values = this->findSuit(cRestriction);

        winningCard = max_element(values.begin(), values.end());
        if(*winningCard == -1)
        {
            values = this -> findSuit(this -> leadCard[0]);
        }
    }

    winningCard = max_element(values.begin(), values.end());

    return *winningCard;
}

void State::findWinningPlayer()
{
    int winningCard = findWinningCard();
    int winningPlayer = (this -> leadingPlayer + winningCard) % 4;
    this -> player = winningPlayer;
    this -> leadingPlayer = winningPlayer;
}

void State::testTrick()
{

    //find(this->trick.begin(),this->trick.end(), "") == this->trick.end()
    if(not this->trick.empty())
        if(this->trick.size() == 4)
        {
            this -> numTricks++;
            findWinningPlayer();
            if(this -> leadingPlayer % 2 == 0)
            {
                this -> points[0]++;
            }
            else
            {
                this -> points[1]++;
            }

            this -> trick.clear();
            this -> leadCard = "";
        }
}

bool State::handsAreEmpty()
{
    for(int i = 0; i < hands->size(); i ++)
    {
        if (not this->hands[i].empty())
            return false;
    }

    return true;
}

int State::evalTricks()
{
    int leadingTeam = this->owningPlayer % 2;
    int score = this->points[leadingTeam];
    return score;
}

void State::setOwningPlayer(int owningPlayer)
{
    this->owningPlayer = owningPlayer;
}

void State::createHash()
{
    unsigned long hashSum = 0;

    for(int i = 0; this->hands->size(); i++)
    {

        for(auto card = this->hands[i].begin(); card != this->hands[i].end(); card++)
        {
            string c = *card;
            unsigned long val = DECK_MAP.at(c);
            hashSum += val;
        }

        this -> hash[i] = hashSum;

        hashSum = 0;
    }

    for(auto card = this->trick.begin(); card != this->trick.end(); card++)
    {


        if(*card != "")
        {
            string c = *card;
            unsigned long val = DECK_MAP.at(c);
            hashSum += val;
        }

    }

    hashSum += ((unsigned long)this->player) << 52;
    hashSum += ((unsigned long)this->leadingPlayer) << 54;

    unsigned long hashLeadCard = findInVector(DECK, this->leadCard);
    hashLeadCard = hashLeadCard << 56;

    hashSum += hashLeadCard;

    this -> hash[5] = hashSum;
}

State State::copy()
{
    State newState = State(this->hands, this->player, this->leadCard, this->leadingPlayer, this->trick,
                           this->points,  this->numTricks, this->cardsPlayed, this->restriction, this->bid);

    newState.setOwningPlayer(this->owningPlayer);
    newState.createHash();

    return newState;
}

unsigned long * State::getHash()
{
    return this->hash;
}
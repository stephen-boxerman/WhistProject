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
#import <unordered_set>

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

State::State(unordered_set<string> (&hands)[4], int player, string leadCard, int leadingPlayer, list<string> &trick, int (&points)[2],
        int numTricks, list<string> &cardsPlayed, string restriction, string bid)
{
    this->player = player;
    this->owningPlayer = this->player;
    this->leadCard = leadCard;
    this->leadingPlayer = leadingPlayer;
//    this->numTricks = numTricks;
    this->restriction = restriction;
    this->bid = bid;

    this->hands[0] = unordered_set<string>(hands[0].begin(), hands[0].end());
    this->hands[1] = unordered_set<string>(hands[1].begin(), hands[1].end());
    this->hands[2] = unordered_set<string>(hands[2].begin(), hands[2].end());
    this->hands[3] = unordered_set<string>(hands[3].begin(), hands[3].end());
    this->trick.operator=(trick);
    this->cardsPlayed= unordered_set<string>(cardsPlayed.begin(), cardsPlayed.end());
    this->points[0] = points[0];
    this->points[1] = points[1];
}

State::~State()
{

}

unordered_set<string> State::getHand(int hand) {return this->hands[hand];}

void State::setPlayer(int player) {this->player = player;}

int State::getPlayer() {return this->player;}

void State::setLeadCard(string card) {this->leadCard = card;}

string State::getLeadCard() {return this->leadCard;}

unordered_set<string> * State::getCardsPlayed() {return &(this->cardsPlayed);}

void State::setRestriction(string res) {this -> restriction = res;}

void State::setBid(string bid) {this->bid = bid;}

void State::removeFromHand(int hand, string card)
{
   this -> hands[hand].erase(card);
}

void State::addToHand(int hand, string card)
{
    auto isFound = hands[hand].find(card);
    if(isFound != hands[hand].end()) this-> hands[hand].insert(card);
}

void State::addToCardsPlayed(string card) {this -> cardsPlayed.insert(card);}

void State::addToTrick(string card) {this -> trick.emplace_back(card);}

void State::removeFromCardsPlayed(string card) {this->cardsPlayed.erase(card);}

void State::removeFromTrick() {if(not trick.empty()) this -> trick.pop_back();}

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
    int pointsMade = this->points[leadingTeam];
    int trickGoal;
    int score = 0;
    //pointsMade -= 6;
    if(this->bid != "p")
    {
        trickGoal = (int)bid[0];
        if(pointsMade >= trickGoal) {score+=pointsMade;}
        else {score -= trickGoal;}
    }
    else if(pointsMade > 0) {score += pointsMade;}

    if(this->bid.size() == 3) {score *= 2;}

    return score;

}

void State::createHash()
{
    unsigned long long hashSum = 0;

    for(int i = 0; i < 4; i++)
    {
        for(unordered_set<string>::iterator card = this->hands[i].begin(); card != this->hands[i].end(); card++)
        {
            string c = *card;
            unsigned long long val = DECK_MAP.at(c);
            hashSum += val;
        }

        this -> hash.push_back(hashSum);

        hashSum = 0;
    }

    for(auto card = this->trick.begin(); card != this->trick.end(); card++)
    {


        if(*card != "")
        {
            string c = *card;
            unsigned long long val = DECK_MAP.at(c);
            hashSum += val;
        }

    }

    hashSum += ((unsigned long long)this->player) << 52;
    hashSum += ((unsigned long long)this->leadingPlayer) << 54;

    unsigned long hashLeadCard = findInVector(DECK, this->leadCard);
    hashLeadCard = hashLeadCard << 56;

    hashSum += hashLeadCard;

    this -> hash.push_back(hashSum);
}


State * State::copy()
{

    State * newState = new State;

    newState->player = this->player;
    newState->owningPlayer = this->player;
    newState->leadCard = this->leadCard;
    newState->leadingPlayer = this->leadingPlayer;
    newState->numTricks = this->numTricks;
    newState->restriction = this->restriction;
    newState->bid = this->bid;

    newState->hands[0] = this->hands[0];
    newState->hands[1] = this->hands[1];
    newState->hands[2] = this->hands[2];
    newState->hands[3] = this->hands[3];
    newState->trick.operator=(this->trick);
    newState->cardsPlayed.operator=(this->cardsPlayed);
    newState->points[0] = this->points[0];
    newState->points[1] = this->points[1];

    newState->createHash();

    return newState;
}

list<unsigned long long> * State::getHash()
{
    return &this->hash;
}
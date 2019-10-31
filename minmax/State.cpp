//
// Created by stephen on 10/18/19.
//

#include <iostream>
#include "State.h"
#include <string>
#include <vector>
#include <algorithm>
#include <map>

using namespace std;

map<char, int> CARD_VALUES = {{'2', 2}, {'3', 3}, {'4', 4}, {'5', 5}, {'6', 6}, {'7', 7}, {'8', 8}, {'9', 9},
                                      {'t', 10}, {'J', 11}, {'Q', 12}, {'K', 13}, {'A', 14}};

const map<string, int> POSABLE_BIDS = {{"p", 0}, {"1", 1}, {"1no", 2}, {"2", 3}, {"2no", 4}, {"3", 5}, {"3no", 6},
                                       {"4", 7}, {"4no", 8}, {"5", 9}, {"5no", 10}, {"6", 11}, {"6no", 12}, {"7", 13},
                                       {"7no", 14}};

template < typename type>
int findInVector(const std::vector<type>  & vecOfElements, const type & element)
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

State::State() {};

State::State(vector<vector<string> > hands, int player, string leadCard, int leadingPlayer, vector<string> trick, vector<int> points,
        int numTricks, vector<string> cardsPlayed, string restriction, string bid)
{
    this->player = player;
    this->owningPlayer = this->player;
    this->leadCard = leadCard;
    this->leadingPlayer = leadingPlayer;
    this->numTricks = numTricks;
    this->restriction = restriction;
    this->bid = bid;

    this->hands.operator=(hands);
    this->trick.operator=(trick);
    this->cardsPlayed.operator=(cardsPlayed);
    this->points.operator=(points);
}

vector<string> State::getHand(int hand) {return this->hands[hand];}

void State::setPlayer(int player) {this->player = player;}

int State::getPlayer() {return this->player;}

void State::setLeadCard(string card) {this->leadCard = card;}

string State::getLeadCard() {return this->leadCard;}

void State::setLeadingPlayer(int leadingPlayer) {this -> leadingPlayer = leadingPlayer;}

int State::getLeadingPLayer() {return this -> leadingPlayer;}

vector<string> State::getTrick() {return this -> trick;}

vector<int> State::getPoints() {return this -> points;}

void State::setNumTricks(int numTricks) {this -> numTricks = numTricks;}

int State::getNumTricks() {return this -> numTricks;}

vector<string> State::getCardsPlayed() { return this -> cardsPlayed;}

void State::setRestriction(string restriction) {this -> restriction = restriction;}

string State::getRestriction() {return this -> restriction;}

void State::setBid(string bid) {this -> bid = bid;}

string State::getBid() {return this -> bid;}



void State::removeFromHand(int hand, string item)
{
    remove(hands[hand].begin(), hands[hand].end(), item);
}

void State::addToHand(int hand, string card, int position)
{
    hands[hand].emplace(hands[hand].begin() + position, card);
}

void State::addToCardsPlayed(string card) {this -> cardsPlayed.emplace_back(card);}

void State::addToTrick(string card) {this -> trick.emplace_back(card);}

void State::removeFromCardsPlayed() {this->cardsPlayed.pop_back();}

void State::removeFromTrick() {this -> trick.pop_back();}

vector<int> State::findSuit(char suit, int defaultVal)
{
    vector<int> card_vals;
    for(auto it = this->trick.begin(); it < this -> trick.end(); it++)
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
    vector<int> values;
    vector<int>::iterator winningCard;

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
    for(auto it = this -> hands.begin(); it < this -> hands.end(); it++)
    {
        vector<string> hand = *it;
        vector<string> emptyHand = {"", "", "", "", ""};
        bool handIsEmpty = (*it == emptyHand);
        if (not handIsEmpty)
        {
            return false;
        }
    }

    return true;
}

int State::evalTricks()
{
    int leadingTeam = this->owningPlayer % 2;
    int score = this->points[leadingTeam];
    return score;
}

void State::printHands()
{
    for(vector<vector<string>>::iterator it = hands.begin(); it < hands.end(); it++)
    {
        for (vector<string>::iterator it2 = it->begin(); it2 < it->end(); it2++) {
            cout << *it2<<" ";
        }

        cout<<endl;
    }
}

State State::copy()
{
    State newState = State();
    newState.hands = this->hands;
    newState.player = this->player;
    newState.owningPlayer = this->owningPlayer;
    newState.leadCard = this -> leadCard;
    newState.leadingPlayer = this -> leadingPlayer;
    newState.numTricks = this -> numTricks;
    newState.trick = this -> trick;
    newState.cardsPlayed = this -> cardsPlayed;
    newState.points = this -> points;
    newState.restriction = this->restriction;
    newState.bid = this->bid;

    return newState;
}
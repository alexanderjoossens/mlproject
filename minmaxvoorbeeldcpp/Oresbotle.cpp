#include "Oresbotle.hpp"
#include <optional>
#include <vector>
#include <ostream>
#include <iostream>
#include <algorithm>

Oresbotle::Oresbotle() {
    table_ = TranspositionTable();
}

std::string Oresbotle::name() const { return "oresbotle"; }

std::string Oresbotle::version() const { return "1.0"; }

std::string Oresbotle::author() const { return "Orestis Lomis"; }

void Oresbotle::newGame() {}

PrincipalVariation  Oresbotle::pv(const Board& board, const TimeInfo::Optional& timeInfo) {
    // search the board
    // return the principal variation
    Board b = board;
    std::tuple<int, std::deque<Move>> result = negascout(b, 5, -10000, 10000);
    std::deque<Move> moves = std::get<1>(result);
    int score = std::get<0>(result);
    (void)timeInfo;
    return PrincipalVariation(moves, score);
}

int Oresbotle::evaluate(const Board& board) const {
    // evaluate the board
    // return a score
    // score is a number between -10000 and 10000
    // 0 is a draw
    // -10000 is a loss
    // 10000 is a win
    // initialize score to 0
    int score = 0;
    int matWhite = 0;
    int matBlack = 0;
    bool whitePair = false;
    bool oppoPair = false;
    int posWhite = 0;
    int posBlack = 0;
    int pawnsWhite = 0;
    int pawnsBlack = 0;
    for (int i = 0; i < 64; i++) {
        Piece::Optional p = board.piece(Square::fromIndex(i).value());
        if (p.has_value()) {
            Piece piece = p.value();
            if (piece.color() == PieceColor::White) {
                // add score for each piece type
                // add score for each piece position

            
                // we give the bishop a slightly higher score than the knight, because the bishop is generally regarded as more powerful; additionally the trickyness of the knight is a non-factor in chess engines, because they can calculate all possible moves
                if (piece.type() == PieceType::Pawn) {
                    // add score for each pawn
                    matWhite += 100;
                    pawnsWhite += pawnTable[i];
                } else if (piece.type() == PieceType::Knight) {
                    // add score for each knight
                    matWhite += 325;
                    posWhite += knightTable[i];
                } else if (piece.type() == PieceType::Bishop) {
                    // add score for each bishop
                    matWhite += 350;
                    posWhite += bishopTable[i];
                    if (whitePair) {
                        posWhite += 50;
                    } else {
                        whitePair = true;
                    }
                } else if (piece.type() == PieceType::Rook) {
                    // add score for each rook
                    matWhite += 500;
                    posWhite += rookTable[i];
                } else if (piece.type() == PieceType::Queen) {
                    // add score for each queen
                    matWhite += 900;
                    posWhite += queenTable[i];
                }

            } else {
                // opponent piece
                if (piece.type() == PieceType::Pawn) {
                    // add score for each pawn
                    matBlack -= 100;
                    pawnsBlack -= pawnTable[63-i];
                } else if (piece.type() == PieceType::Knight) {
                    // add score for each knight
                    matBlack -= 325;
                    posBlack -= knightTable[i];
                } else if (piece.type() == PieceType::Bishop) {
                    // add score for each bishop
                    matBlack -= 350;
                    posBlack -= bishopTable[63-i];
                    if (oppoPair) {
                        posBlack -= 50;
                    } else {
                        oppoPair = true;
                    }
                } else if (piece.type() == PieceType::Rook) {
                    // add score for each rook
                    matBlack -= 500;
                    posBlack -= rookTable[63-i];
                } else if (piece.type() == PieceType::Queen) {
                    // add score for each queen
                    matBlack -= 900;
                    posBlack -= queenTable[i];
                }
            }
        }

    }
    score += posWhite;
    score += posBlack;

    // interpolate material and add king score
    int matSum = matWhite - matBlack;
    double midWeight = (matSum - matMin) / (matMax - matMin);
    if (midWeight < 0) {
        midWeight = 0;
    } else if (midWeight > 1) {
        midWeight = 1;
    }
    double endWeight = 1 - midWeight;
    int pawnsScore = pawnsWhite + pawnsBlack;
    pawnsScore += pawnsScore*endWeight; // give more weight to pawns in the endgame
    score += (matWhite + matBlack);
    if (board.turn() == PieceColor::Black) { score = -score; }

    // add king score
    Square kingSquareWhite = board.kingSquare(board.turn());
    Square kingSquareBlack = board.kingSquare(!board.turn());
    score += kingTableMid[kingSquareWhite.index()]*midWeight + kingTableEnd[kingSquareWhite.index()]*endWeight;
    score -= kingTableMid[kingSquareBlack.index()]*midWeight + kingTableEnd[kingSquareBlack.index()]*endWeight;

    // add a negative effect if the white is in check
    if (board.isAttacked(kingSquareWhite, !board.turn())) {
        score -= 100;
    }

    // TODO
    // pawn structure analysis
    // negative effect for isolated and doubled pawns
    // positive effect for passed pawns
    // negative effect for backward pawns
    // positive effect for rooks on open files


    // std::cout << "board: " << board << std::endl;
    // std::cout << "score: " << score << std::endl;
    return score;
}

std::tuple<int, std::deque<Move>> Oresbotle::negascout(Board& board, int depth, int alpha, int beta) {
    // std::cout << "depth: " << depth << std::endl;
    // TODO: iterative deepening
    if (depth <= 0) {
        // return std::make_tuple(quiescence(board), std::deque<Move>());
        return std::make_tuple(evaluate(board), std::deque<Move>());
    } else {
        std::vector<Move> moves;
        // Board orig = board;
        board.pseudoLegalMoves(moves);
        std::deque<Move> bestMoves;
        int bestScore = -10000;
        int a = alpha;
        int b = beta;
        for (int d = 1; d <= depth; d++) {
            
            std::sort(moves.begin(), moves.end(), [](const Move& a, const Move& b) {
                return a.score() > b.score();
            });
            bestScore = -10000;
            // std::cout << "board: " << board << std::endl;
            // for (Move move : moves) {
            // CastlingRights castlingRights = board.castlingRights();
            // Square::Optional enPassantSquare = board.enPassantSquare();
            for (int i = 0; i < (int)moves.size(); i++) {
                Move move = moves.at(i);
                // std::cout << "move: " << move << std::endl;
                int score;
                std::deque<Move> newMoves;
                // while (!moves.empty()) {
            //     Move move = Board::popMax(moves);
                // // std::cout << "move: " << move << std::endl;
            // // std::cout << "get from" << std::endl;
            // Square from = move.from();
            // // std::cout << "get to" << std::endl;
            // Square to = move.to();
            // // std::cout << "get piece" << std::endl;
            // Piece::Optional piece = board.piece(from);
            // // std::cout << "get captured piece" << std::endl;
            // Piece::Optional capturedPiece = board.piece(to);
            // bool epCapture = move.enpassant();
            // // std::cout << "get castling" << std::endl;
            // int castle = move.castling();
            // // std::cout << "making move" << std::endl;
            // board.makeMove(move);
            // std::cout << "move made" << std::endl;
                Board newBoard = board;
                newBoard.makeMove(move);
                // uint64_t hash = table_.hash_value(newBoard);
                // // std::cout << "board: " << newBoard << std::endl;
                // // std::cout << "hash: " << hash << std::endl;
                // Entry* entry = table_.lookup(hash);
                // if (entry == nullptr || (entry->depth() < d || entry->alpha() >= alpha || entry->beta() >= beta)) {
                    if (newBoard.isInCheck(!newBoard.turn())) {
                    // if (board.isInCheck(!board.turn())) {
            //     board.undoMove(from, to, piece, capturedPiece, castlingRights, enPassantSquare, epCapture, castle);
                // if (board != orig) {
                //     std::cout << "move: " << move << " did not undo correctly" << std::endl;
                //     std::cout << "board: " << board << std::endl;
                //     std::cout << "orig: " << orig << std::endl;
                //     std::cout << "move castle value: " << move.castling()  << std::endl;
                //     std::cout << "move enpassant value: " << move.enpassant()  << std::endl;
                // }
                // std::cout << "move undone" << std::endl;
                        continue;
                    }
                    std::tuple<int, std::deque<Move>> result = negascout(newBoard, d - 1, -beta, -alpha);
                    // table_.add_entry(hash, d, alpha, beta, std::get<0>(result), std::get<1>(result));

                    score = -std::get<0>(result);
                    newMoves = std::get<1>(result);
                    // if (static_cast<unsigned long int>(std::distance(table_.getTable().begin(), table_.getTable().end())) > hashInfo().value().maxSize) {
                        // table_.deleteRandomEntry();
                    // }
                    // table_.add_entry(hash, d, alpha, beta, score, newMoves);
                // } else {
                //     // std::cerr << "found entry" << std::endl;
                //     score = entry->score();
                //     newMoves = entry->bestMoves();
                // }
                // std::tuple<int, std::deque<Move>> result = negascout(board, depth - 1, -beta, -alpha);
            // board.undoMove(from, to, piece, capturedPiece, castlingRights, enPassantSquare, epCapture, castle);
            // if (board != orig) {
            //     std::cout << "move: " << move << " did not undo correctly" << std::endl;
            //     std::cout << "board: " << board << std::endl;
            //     std::cout << "orig: " << orig << std::endl;
            //     std::cout << "move castle value: " << move.castling()  << std::endl;
            //     std::cout << "move enpassant value: " << move.enpassant()  << std::endl;
            // }
            // std::cout << "move undone" << std::endl;
                
                move.setScore(score);
                moves[i] = move;
                newMoves.push_front(move);
                if (score > bestScore || (bestScore == -10000 && newMoves.size() > bestMoves.size())) {
                    bestScore = score;
                    bestMoves.swap(newMoves);
                    // std::cout << "move: " << move << std::endl;
                }
                if (score > alpha) {
                    alpha = score;
                }
                if (alpha >= beta) {
                    break;
                }
            }

            if (bestScore == -10000 && !board.isInCheck(board.turn())) {
                bestScore = 0;
            }
            alpha = a;
            beta = b;
            // std::cout << "bestScore: " << bestScore << std::endl;
        // std::cout << "bestMoves size: " << bestMoves.size() << std::endl;
        // std::cout << "bestMoves: " << std::endl;
        // for (Move mv : bestMoves) {
        //     std::cout << mv << std::endl;
        // }
        }
    
        return std::make_tuple(bestScore, bestMoves);
    }
}

int Oresbotle::quiescence(Board& board) { // FIXME: this is not working correctly, not gonna use it for now
    std::vector<Move> moves;
    board.pseudoLegalMoves(moves);
    std::sort(moves.begin(), moves.end(), [](const Move& a, const Move& b) {
                return a.score() > b.score();
    });
    for (Move move : moves) {
        Board newBoard = board;
        if (move.score() >= 10) {
            newBoard.makeMove(move);
            if (!newBoard.isInCheck(!newBoard.turn())) {
                return quiescence(newBoard);
            }
        }
    }
    return evaluate(board);
}



std::optional<HashInfo> Oresbotle::hashInfo() const {
    HashInfo info;
    info.defaultSize = 0;
    info.minSize = 0;
    info.maxSize = table_.size();
    return info;
}

void  Oresbotle::setHashSize(std::size_t size) {
    table_.setSize(size);
}

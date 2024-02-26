package hws.hw5;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

import hws.hw4.Letter;

public class TestBoard {
    @Test
    public void testGettersSetters() {
        Board board = new Board(new int[] {1, 1}, "words.txt");
        assertArrayEquals(board.getEntries(), new Letter[2]);

        Letter[] newArr = {new Letter('a', 1), new Letter('b', 1)};
        board.setEntries(newArr);
        assertArrayEquals(board.getEntries(), newArr);
    }

    @Test
    public void testReadWord() {
        Board board = new Board(new int[] {1, 1, 1, 1, 1, 1}, "words.txt");
        Letter[] newArr = {null, new Letter('c', 1), new Letter('a', 1), null,
                null, null};
        board.setEntries(newArr);

        board.play(new Letter('t', 1), 3);
        assertEquals(board.readBoardWord(), "cat");
        assertArrayEquals(newArr, new Letter[] {null, new Letter('c', 1),
                new Letter('a', 1), null, null, null});

        board.setEntries(newArr);
        board.play(new Letter('t', 1), 4);

        Letter[] correctArr = {null, new Letter('c', 1), new Letter('a', 1),
                null, new Letter('t', 1), null};
        assertArrayEquals(correctArr, board.getEntries());

        assertEquals(board.readBoardWord(), "ca-t");
    }

    @Test
    public void testValidation() {
        Board board = new Board(new int[] {1, 1, 1, 1, 1, 1}, "/home/tabulate/school/freshman/sem2/cs159/src/hws/hw5/words.txt");

        assertTrue(board.wordValidation("cast"));
    }

    @Test
    public void testBoardScore() {
        Board board = new Board(
                new Letter[] {new Letter('s', 1), new Letter('p', 1),
                        new Letter('o', 1), new Letter('n', 2),
                        new Letter('g', 1)},
                new int[] {2, 1, 1, 2, 3}, "/home/tabulate/school/freshman/sem2/cs159/src/hws/hw5/words.txt");
        assertEquals(board.getBoardScore(), 11);
    }

    @Test
    public void testToString() {
        Board board = new Board(
                new Letter[] {new Letter('s', 1), null, new Letter('o', 1),
                        new Letter('n', 2), null},
                new int[] {2, 1, 1, 2, 3}, "/home/tabulate/school/freshman/sem2/cs159/src/hws/hw5/words.txt");
        assertEquals(board.toString(), "s:1, -, o:1, n:2, -, ");
    }
}

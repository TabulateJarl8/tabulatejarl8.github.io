---
title: "College Range Assignment"
date: 2024-01-17T19:10:05-05:00
draft: false
tags: ["assembly", "python"]
---

A friend of mine is enrolled in a college intro to programming course. This course had a very simple entrance test: they needed to write a program in any language to display the numbers 5-60 prefixed with "number ", like so:

```txt
number 5
number 6
number 7
number 8
...
number 60
```

After he told me about this assignment, I thought that it was pretty funny, and I wanted to write it in assembly as a joke. I started off with stealing some integer printing code that I had written for another project.

{{< collapse "The integer printing code" >}}
{{< highlight asm "linenos=table" >}}
; Print "number i" for i in range(5,60)
section .data
	str_buffer db 0 ; for printing integers

section .text
	global _start

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Integer printing system ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

calculate_ten_power:
	; calculate the power of 10 that corresponds to an integer
	; for example, 100 for 543, 1000 for 8956, and 10000 for 15236

	; returns the integer in rcx

	; rsp is the return address, add 8 to get the argument
	mov rcx, [rsp+8] ; rcx should be the integer to find the power of 10 for

	mov rax, 1 ; we need to calculate the power of 10 that corresponds to rcx
	; for example 100 for 543 and 1000 for 8753
	mov rbx, 10
	calculate_ten:
		mul rbx
		cmp rax, rcx
		jg finish_power_ten ; if number is greater than target, divide by 10 and ret
		jmp calculate_ten

	finish_power_ten:
		; divide ax by 10 to finish the calculation
		xor rdx, rdx
		div rbx
		; now rax contains the power of 10
		mov rcx, rax
	ret


print_digit:
	push rcx
	mov rcx, [rsp+16]
	add rcx, '0' ; convert digit to ASCII

	mov byte [str_buffer], cl ; assign lower 8 bits of rcx to buffer

	mov rsi, str_buffer ; buffer pointer
	mov rax, 1 ; write
	mov rdi, 1 ; stdout
	mov rdx, 1 ; len
	syscall   ; call kernel

	pop rcx ; restore rcx

	ret


print_integer:
	; takes the integer in from rax
	push rax ; push rax it for the next function to consume
	call calculate_ten_power ; power of 10 is now in rcx

	pop rax ; mov the argument (number to print) that was pushed into rax

	iter_number:
		; num_to_print: rax
		; base_10_place: rcx
		; formula for accessing number: (num_to_print // base_10_place) % 10
		; base_10_place is the power of 10 that corresponds to the place of number to print
		; using 123 for example, 100 will get the 1, 10 will get the 2, and 1 will get the 3

		; first, make sure we have a copy of rax
		push rax

		; 10 for use in modulo
		mov rbx, 10

		; next, floor divide rax by rcx
		xor rdx, rdx
		div rcx
		; result is stored in rax, mod 10
		; clear out rdx because thats where remainder is stored
		xor rdx, rdx
		div rbx

		; rdx now contains our digit to print
		push rdx
		call print_digit
		add rsp, 8 ; remove the rdx that never got popped from print_digit from the stack


		; check if rcx is equal to 1. if so, we just did the last digit
		mov rax, 1
		cmp rax, rcx
		je exit_print_integer

		; divide out power of 10 by 10 to get the next digit
		xor rdx, rdx
		mov rbx, 10
		mov rax, rcx

		div rbx
		mov rcx, rax

		; restore our original number to print
		pop rax

		; loop to iter_number until rcx is 1 (we've done the last digit)
		jmp iter_number

	exit_print_integer:
	pop rax ; pop off our original number so that we return to the correct address

	ret

_start:
	mov rax, 60
	mov rdi, 0
	syscall ; call kernel
{{< /highlight >}}
{{< /collapse >}}

After setting this up, I wrote a quick assembly program to iterate over the numbers 5-40 and print each one:

{{< highlight asm "linenos=table,hl_lines=2-3 15 27-29 43" >}}
section .data
	line_text db "number "
	line_text_len equ $ - line_text

	str_buffer db 0 ; for printing integers

section .text
	global _start

; integer printing code here

_start:
	mov rcx, 5
	loop_start:	
		cmp rcx, 61 ; if at 61, jump to exit
		je exit

		push rcx

		; print line text
		mov rax, 1
		mov rdi, 1
		mov rsi, line_text
		mov rdx, line_text_len
		syscall

		mov rax, [rsp] ; put current increment in rax to print

		call print_integer

		; print newline
		push 0xa ; newline
		mov rax, 1
		mov rdi, 1
		mov rsi, rsp
		mov rdx, 1
		syscall

		; pop newline from stack
		add rsp, 8
		pop rcx

		inc rcx
		jmp loop_start

	exit:
		mov rax, 60
		mov rdi, 0
		syscall ; call kernel
{{< /highlight >}}

--- 
This was pretty simple, and I felt good about it, so I sent it to my friend. He then responded with, "Unfortunately a requirement was that it be 'significantly less than 55 lines'". This could only be taken as a challenge, of course. He suggested that I hardcode a block of memory to contain the numbers and text that I have to print, and I thought that was a great idea, so I got to work. 

## Generating the data
My first task was to write a throwaway Python script to generate this data. After some fiddling, I came up with this:

{{< highlight python "linenos=table" >}}
import textwrap
data = ''

# "number {i}\n"
for num in [f'6e756d62657220{str(i).encode().hex():0<4}0a' for i in range(5, 61)]:
	data += ', '.join(['0x' + split for split in textwrap.wrap(num, 2)]) + ', '

data = data.rstrip(', ')

print(data)
{{< /highlight >}}

This program is pretty simple if you break it down. Let's focus on the list comprehension first:

{{< highlight python "linenos=table" >}}
	[f'6e756d62657220{str(i).encode().hex():0<4}0a' for i in range(5, 61)]
{{< /highlight >}}

Inside the list comprehension, you can see the numbers we're iterating over in `range(5, 61)`. For every number in this range, we add a new string to the list:

{{< highlight python "linenos=table" >}}
	f'6e756d62657220{str(i).encode().hex():0<4}0a'
{{< /highlight >}}

The first chunk of this string, `6e756d62657220`, represents the text prefixing the number ("number ") in hex. Then, we convert the current number in the loop iteration to a string, and generate the ASCII hex representation for each of it's digits. For example, `str(12).encode().hex()` would return `3132`, since 1 in hex is `0x31` and 2 is `0x32`. You may have noticed the `:0<4` at the end of the f-string. This fixes a bug that I discovered. I want each line to be the same length so that it's super easy to print in assembly, however single digit numbers are only one hex number, while double digit numbers are two hex digits. To solve this, I introduced null-padding into the numbers. This means that if a number is only 1 hex number long, I add a null byte after it. This null byte is not rendered by the terminal, so it shouldn't interfere with how the display is formatted. For example, if we have the number 7 (0x37), this little part of the f-string will add 0x00 after it, giving us a 4 byte long string of `0x37, 0x00`. The only part remaining is the `0a` at the end of the string, which is hex for a newline (`\n`). This covers the list comprehension of the Python. Next is the second step:

{{< highlight python "linenos=table" >}}
	data += ', '.join(['0x' + split for split in textwrap.wrap(num, 2)]) + ', '
{{< /highlight >}}

This part is pretty simple as well. We take each sequence of hex digits that were generated from the previous step (e.g. `3132`), and we convert them into a format that assembly can read. First, we use the textwrap module (very strange usage of this module but I guess it works) to split the data into 2 digit long chunks. For example, `'3132'` would be split into `['31', '32']`. We then prepend `0x` to each of these strings to tell the assembly that this is a hexadecimal number and not a base 10 number. The rest of the code on that line just strings together each of these new numbers with commas, giving you a final result of `0x31, 0x32`.

## Writing the assembly program

Next step was to write the program. I had a pretty strong mental image of how this should go:

1. Initialize the hardcoded data
2. Check if the address that I'm reading from is past the bounds of the data
   - If it is, exit
   - If it's not, continue
3. Print a set amount of data from the memory
4. Increment the address that I'm reading from and loop

I started writing, and after a while I came up with a very basic implementation. I had a counter that incremented until it was equal to the length of the data block, and when it was, it exited. However, I realized that I could do some math to replace the counter entirely, and this removed a few lines of code. Here's what I ended up with:

{{< highlight asm "linenos=table,hl_lines=2 8 12-14 19" >}}
section .data
	numbers db 0x6e, 0x75, 0x6d, ...
	numbers_len equ $ - numbers
section .text
	global _start

_start:
	lea rsi, [numbers] ; load address of numbers into rsi

	printing_loop:

		lea rdi, [numbers + numbers_len]
		cmp rsi, rdi
		je exit
		mov rdi, 1
		mov rax, 1
		mov rdx, 10 ; the number of bytes to print from rsi
		syscall
		add rsi, 10
		jmp printing_loop

	exit:
		mov rax, 60 ; exit
		mov rdi, 0
		syscall
{{< /highlight >}}

As you can see, this implementation worked and it was significantly shorter than the previous implementation due to it's hardcoded nature. Line 2 initializes the data, line 8 loads the address of the data into `rsi` before we start the loop, and then we start printing. Lines 12-14 are for bounds checking. We load the address of `numbers` plus the length of that block of data into `rdi`, and then compare it with the address we're currently reading from, `rsi`. If they're equal, that means we've read all of the data, and we can exit. If not, we continue and load data into the appropriate registers in order to print 10 bytes from our current memory address. Think of it as taking 10 bytes at a time from our huge list of bytes. Then, we print these 10 bytes to the screen and end up with something like `number 12`. Then, we check if there's another 10 bytes, available, and if there are, we continue doing this. However, I was really invested now and wanted to try and make it as short as possible, so I looked for ways to optimize it. Even when I remove linebreaks and put labels on the same lines as code, I still end up with this:

{{< highlight asm "linenos=table,hl_lines=2 8 12-14 19" >}}
section .data
	numbers db 0x6e, 0x75, 0x6d, ...
	numbers_len equ $ - numbers
section .text
	global _start
_start: lea rsi, [numbers] ; load address of numbers into rsi
	printing_loop: lea rdi, [numbers + numbers_len]
		cmp rsi, rdi
		je exit
		mov rdi, 1
		mov rax, 1
		mov rdx, 10 ; the number of bytes to print from rsi
		syscall
		add rsi, 10
		jmp printing_loop
	exit: mov rax, 60 ; exit
		mov rdi, 0
		syscall
{{< /highlight >}}

This is 18 lines, which is better than 25 but I still felt like I could do even better. I kept analyzing, and then all of a sudden, I saw it in a way I hadn't seen before, and I quickly moved some stuff around. Here's the final product:

{{< highlight asm "linenos=table,hl_lines=2 19-20" >}}
section .data
	numbers db 0x6e, 0x75, 0x6d, ..., 0x0
section .text
	global _start

_start:
	lea rsi, [numbers] ; load address of numbers into rsi

	printing_loop:

		mov rdi, 1
		mov rax, 1
		mov rdx, 10 ; print 10 bytes. rsi is already loaded
		syscall

		; increment rsi by 10. this changes the address to start at the next number, since "line xx\n" is 8 bytes long
		add rsi, 10

		cmp byte [rsi], 0 ; check if the first byte in the next sequence is null
		jne printing_loop ; if it isn't we haven't reached the end, keep printing

		mov rax, 60 ; exit
		mov rdi, 0
		syscall
{{< /highlight >}}

You may have noticed something a little different, which is the trailing null byte at the end of the data block. I realized that the first byte in the chunk of 10 will never be null unless I explicitly set it, since the first thing in each line is the letter "n" (`0x6e`). After adding this null byte, I could get rid of the `numbers_len` variable completely and all of the extra lines that came along with it. The flow of the program is still mostly the same. Instead of bounds checking first, I print our 10 bytes first. Then, I increment our address by 10 and check if the first byte in this next chunk of 10 is `0x0`. If it is **not**, then that means we're not done and we jump back up to the printing loop. This little inversion of checking saves us an extra line of code because we don't have to `jmp printing_loop` at the bottom of the loop, this is just done if we're not finished. If we are finished, the program will continue reading top down, skipping the jump to `printing_loop`, and we'll exit with status code 0. When we remove all blank lines and we collapse labels, we end up with a final total of 15 lines, which is pretty good in my opinion. The full code for all of these files can be found below:

https://github.com/TabulateJarl8/random-junk/tree/94c72e4d746f0e7d9116e38230301fffaee47b82/asm/range_print
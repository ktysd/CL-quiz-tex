#!/bin/sh

if [ $# -eq 0 ]; then
    echo "Usage:"
    echo " \$ ./Make.sh serial_number.tex\n"
    exit
fi

serial_number=`basename $1 .tex`
tex_src="${serial_number}.tex"
tex_dvi="${serial_number}.dvi"
answer_pdf="${serial_number}.pdf"
quiz_pdf="CL_${serial_number}.pdf"
raw_csv="${serial_number}.quiz"
CL_csv="CL_${serial_number}.csv"

switch_tex="lib/DRAFT_SWITCH.tex"
### Generate Quiz PDF
echo "\\Draftmodefalse"     >  ${switch_tex}
echo "\\hideanswerlisttrue" >> ${switch_tex}
platex ${tex_src}; platex ${tex_src};
dvipdfmx ${tex_dvi} -o ${quiz_pdf}

### Generate Answer PDF
echo "\\Draftmodetrue"       >  ${switch_tex} 
echo "\\hideanswerlistfalse" >> ${switch_tex}
platex ${tex_src}; platex ${tex_src};
dvipdfmx ${tex_dvi} -o ${answer_pdf}

### Generate C-Learning upload CSV
python3 Setup.py ${raw_csv} ${CL_csv}

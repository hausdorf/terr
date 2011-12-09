%%
%% This is file `myclass.cls',
%%
%% For the copyright see the source file.
%% 
%% Any modified versions of this file must be renamed
%% with new filenames distinct from myclass.cls.
%% 
%% This file is distributed in the hope that it will be useful,
%% but WITHOUT ANY WARRANTY; without even the implied warranty of
%% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
%%
%% \CharacterTable
%%  {Upper-case    \A\B\C\D\E\F\G\H\I\J\K\L\M\N\O\P\Q\R\S\T\U\V\W\X\Y\Z
%%   Lower-case    \a\b\c\d\e\f\g\h\i\j\k\l\m\n\o\p\q\r\s\t\u\v\w\x\y\z
%%   Digits        \0\1\2\3\4\5\6\7\8\9
%%   Exclamation   \!     Double quote  \"     Hash (number) \#
%%   Dollar        \$     Percent       \%     Ampersand     \&
%%   Acute accent  \'     Left paren    \(     Right paren   \)
%%   Asterisk      \*     Plus          \+     Comma         \,
%%   Minus         \-     Point         \.     Solidus       \/
%%   Colon         \:     Semicolon     \;     Less than     \<
%%   Equals        \=     Greater than  \>     Question mark \?
%%   Commercial at \@     Left bracket  \[     Backslash     \\
%%   Right bracket \]     Circumflex    \^     Underscore    \_
%%   Grave accent  \`     Left brace    \{     Vertical bar  \|
%%   Right brace   \}     Tilde         \~}
%%
\NeedsTeXFormat{LaTeX2e}[1994/06/01]
\ProvidesClass{myclass}
[2001/01/01 v1.2.1
 My Customized Document Class]
%%  Package include section: %%%%%
\usepackage{latexsym}
%% Cool math font
%\usepackage{euler}
\usepackage{times}
\renewcommand{\sfdefault}{cmss}
%% AMS-LaTeX goodies
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
%% For \includegraphics commands
\usepackage{graphics}
\usepackage[pdftex]{graphicx}
%% To cite urls without them being broken across lines: \url{..}
\usepackage{url}
%% To insert space at the end of a word depending on if punctuation
 %% follows: \xspace
\usepackage{xspace}
\usepackage{fancybox}
%% Special \ifcommands %%%%%
\newif\ifacm@camera
\newif\ifacm@preprint
\newif\ifacm@review
\newif\iffancy
\newcommand{\acm@columnmode}{}
\newcommand{\acm@pointsize}{}
%% THis is very useful. Insert the option
 %% \documentclass[...submission,..]{myclass} in order to have text that
 %% is conditionally inserted if we are in submission mode. 
%%
%% Usage: \submission{text in submission}{Text if not submission}
\newif\ifsubmission
\def\ds@submission{\submissiontrue}
\newcommand{\submission}[2]{\ifsubmission #1 \else #2 \fi}

%% Some general useful commands
%% \mnote is for only backward compatibility. 
\newcommand{\mnote}[1]      {{\marginpar[\hfill$\rhd$]{$\lhd$}
                            $\langle${\sc\bf #1}$\rangle$}}

\newcommand{\note}[1]      {{\marginpar[\hfill$\rhd$]{$\lhd$}
                            $\langle${\sc\bf #1}$\rangle$}}
\long\gdef\boxit#1{\vspace{5mm}\begingroup\vbox{\hrule\hbox{\vrule\kern3pt
      \vbox{\kern3pt#1\kern3pt}\kern3pt\vrule}\hrule}\endgroup}
\newcommand{\bignote}[1]{\shadowbox{%
\begin{minipage}{\textwidth}%
\noindent #1%
\end{minipage}%
}}
\newcommand{\omt}[1]{}
%\newcommand{\etal}{\emph{et al.}\xspace}
%% Puts a raised box on the top of the paper. Should be replaced by a
 %% running header across each page ideally
\newcommand{\ToAppear}[1]{\raisebox{15mm}[10pt][0mm]{\makebox[0mm]{\makebox[\textwidth][c]{#1}}}}  

%% Some shorthand for math symbols
\newcommand{\reals}{{\mathbb R}}
\newcommand{\integers}{{\mathbb Z}}

%% Useful environment for problem definition
\newcommand{\Problem}[3][]{
  \noindent\begin{minipage}{\textwidth}
    \vspace{10pt}
    \noindent\textbf{Problem:} \textbf{\textit{#1}}\\
    \noindent\textbf{Input:}\ #2\\ 
    \noindent\textbf{Output:} #3 
  \end{minipage}
  \vspace{3pt}
}

\newif\ifacm@doublespaced
\newcommand{\acm@optwarning}[1]{%
    \ifacm@camera
        \ClassWarningNoLine{myclass}%
            {#1 option used in camera-ready mode.\MessageBreak
             This violates submission specifications}
    \fi
}
\DeclareOption{onecolumn}{%
    \acm@optwarning{onecolumn}
    \renewcommand{\acm@columnmode}{onecolumn}}
\DeclareOption{twocolumn}{%
    \renewcommand{\acm@columnmode}{twocolumn}}
\DeclareOption{9pt}{%
    \renewcommand{\acm@pointsize}{9pt}}
\DeclareOption{10pt}{%
    \renewcommand{\acm@pointsize}{10pt}}
\DeclareOption{11pt}{%
    \renewcommand{\acm@pointsize}{11pt}}
\DeclareOption{12pt}{%
    \renewcommand{\acm@pointsize}{12pt}}
\DeclareOption{singlespace}{%
    \acm@doublespacedfalse}
\DeclareOption{doublespace}{%
    \acm@doublespacedtrue}
%\newcount\acm@specversion
%\DeclareOption{version1996}{\acm@specversion=1996}
%\DeclareOption{version1994}{\acm@specversion=1994}
%\ExecuteOptions{version1996}
%\DeclareOption{titlepage}{%
%    \OptionNotUsed%
%    \ClassWarningNoLine{myclass}{titlepage option not allowed}}
%\DeclareOption{landscape}{%
%    \OptionNotUsed%
%    \ClassWarningNoLine{myclass}{landscape option not allowed}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions
\PassOptionsToClass{\acm@columnmode}{article}
\ifdim\acm@pointsize>9pt
    \PassOptionsToClass{\acm@pointsize}{article}
\fi
\LoadClass{article}
%\newcommand{\acm@preprinttext}{To appear in the  conference proceedings}
%\newcommand{\preprinttext}[1]{\renewcommand{\acm@preprinttext}{#1}}
%\newcommand{\ifcamera}[1]{\ifacm@review \else #1 \fi}
%\newcommand{\ifreview}[1]{\ifacm@review #1 \fi}
%\newcommand{\ifcameraelse}[2]{\ifacm@review #2 \else #1 \fi}
%\newcommand{\ifreviewelse}[2]{\ifacm@review #1 \else #2 \fi}
\setlength{\textheight}{9.25in}
\setlength{\topmargin}{-0.70in}
\setlength{\headheight}{0.2in}
\setlength{\headsep}{0.250in}
\setlength{\footskip}{0.5in}
\flushbottom
\setlength{\textwidth}{7in}
\setlength{\oddsidemargin}{-0.25in}
\setlength{\evensidemargin}{-0.25in}
\setlength{\columnsep}{2pc}
\setlength{\parindent}{1em}
\renewcommand{\ps@plain}%
    {%
    \ifacm@preprint%
\renewcommand{\@oddhead}{\hfil\textit{\large\acm@preprinttext}\hfil}%
    \else%
\renewcommand{\@oddhead}{}%
    \fi%
    \ifacm@camera%
    \renewcommand{\@oddfoot}{}%
    \else%
\renewcommand{\@oddfoot}{\hfil\textrm{\thepage}\hfil}%
    \fi%
    \renewcommand{\@evenhead}{\@oddhead}%
    \renewcommand{\@evenfoot}{\@oddfoot}%
    }
\renewcommand{\ps@empty}%
    {%
    \ifacm@preprint%
\renewcommand{\@oddhead}{\hfil\textit{\large\acm@preprinttext}\hfil}%
    \else%
\renewcommand{\@oddhead}{}%
    \fi%
    \renewcommand{\@oddfoot}{}%
    \renewcommand{\@evenhead}{\@oddhead}%
    \renewcommand{\@evenfoot}{\@oddfoot}%
    }
\pagestyle{plain}
\newcommand{\acm@setninepoint}{
    \renewcommand\normalsize{%
        \@setfontsize\normalsize\@ixpt\@xpt
        \abovedisplayskip 9\p@ \@plus2\p@ \@minus4\p@
        \abovedisplayshortskip \z@ \@plus3\p@
        \belowdisplayshortskip 6\p@ \@plus3\p@ \@minus3\p@
        \belowdisplayskip \abovedisplayskip
        \let\@listi\@listI}
    \renewcommand\small{%
        \@setfontsize\small\@viipt\@ixpt
        \abovedisplayskip 8.5\p@ \@plus3\p@ \@minus4\p@
        \abovedisplayshortskip \z@ \@plus2\p@
        \belowdisplayshortskip 4\p@ \@plus2\p@ \@minus2\p@
        \def\@listi{\leftmargin\leftmargini
                    \topsep 4\p@ \@plus2\p@ \@minus2\p@
                    \parsep 2\p@ \@plus\p@ \@minus\p@
                    \itemsep \parsep}%
        \belowdisplayskip \abovedisplayskip}
    \renewcommand\footnotesize{%
        \@setfontsize\footnotesize\@viiipt{9.5}%
        \abovedisplayskip 6\p@ \@plus2\p@ \@minus4\p@
        \abovedisplayshortskip \z@ \@plus\p@
        \belowdisplayshortskip 3\p@ \@plus\p@ \@minus2\p@
        \def\@listi{\leftmargin\leftmargini
                    \topsep 3\p@ \@plus\p@ \@minus\p@
                    \parsep 2\p@ \@plus\p@ \@minus\p@
                    \itemsep \parsep}%
        \belowdisplayskip \abovedisplayskip}
    \renewcommand\scriptsize{\@setfontsize\scriptsize\@viipt\@viiipt}
    \renewcommand\tiny{\@setfontsize\tiny\@vpt\@vipt}
    \renewcommand\large{\@setfontsize\large\@xpt\@xiipt}
    \renewcommand\Large{\@setfontsize\Large\@xiipt{14}}
    \renewcommand\LARGE{\@setfontsize\LARGE\@xivpt{18}}
    \renewcommand\huge{\@setfontsize\huge\@xviipt{22}}
    \renewcommand\Huge{\@setfontsize\Huge\@xxpt{25}}
    \selectfont
}
\ifdim\acm@pointsize=9pt
    \acm@setninepoint
\fi
\newcommand{\acm@sectionfont}{}
\newcommand{\sectionfont}[1]{\renewcommand{\acm@sectionfont}{#1}}
%\font\ninsfb = cmssbx11
%\def\@acmtitlestyle{\normalsize\ninsfb}
%\def\section{\@startsection {section}{1}{\z@}{-3.5ex plus -1ex minus
%    -.2ex}{2.3ex plus .2ex}{\@acmtitlestyle}}
%\def\subsection{\@startsection{subsection}{2}{\z@}{-3.25ex plus -1ex minus
%   -.2ex}{1.5ex plus .2ex}{\@acmtitlestyle}}
%\def\subsubsection{\@startsection{subsubsection}{3}{\z@}{-3.25ex plus
%-1ex minus -.2ex}{1.5ex plus .2ex}{\@acmtitlestyle}}
%\def\paragraph{\@startsection
%     {paragraph}{4}{\z@}{3.25ex plus 1ex minus .2ex}{-1em}{\@acmtitlestyle}}
%\def\subparagraph{\@startsection
%     {subparagraph}{4}{\parindent}{3.25ex plus 1ex minus
%     .2ex}{-1em}{\@acmtitlestyle}}

\renewcommand\section{\@startsection {section}{1}{\z@}%
                {-3.5ex \@plus -1ex \@minus -.2ex}%
                {2.3ex \@plus.2ex}%
                {\reset@font\large\sffamily\bfseries\acm@sectionfont}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
                {-3.25ex\@plus -1ex \@minus -.2ex}%
                {1.5ex \@plus .2ex}%
                {\reset@font\large\sffamily\bfseries\acm@sectionfont}}
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                {-3.25ex\@plus -1ex \@minus -.2ex}%
                {1.5ex \@plus .2ex}%
                {\reset@font\normalsize\sffamily\bfseries\acm@sectionfont}}
\renewcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
                {3.25ex \@plus1ex \@minus.2ex}%
                {-1em}%
                {\reset@font\normalsize\sffamily\bfseries\acm@sectionfont}}
\renewcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}%
                {3.25ex \@plus1ex \@minus .2ex}%
                {-1em}%
                {\reset@font\normalsize\sffamily\bfseries\acm@sectionfont}}
%\newcommand{\acm@empty}{}
%\newcommand{\acm@affiliation}{}
%\newcommand{\affiliation}[1]{\renewcommand{\acm@affiliation}{#1}}
%\newcommand{\acm@category}{}
%\newcommand{\category}[1]{\renewcommand{\acm@category}{#1}}
%\newcommand{\acmcategory}[1]{\category{#1}}
%\newcommand{\acm@format}{}
%\newcommand{\format}[1]{\renewcommand{\acm@format}{#1}}
%\newcommand{\acmformat}[1]{\format{#1}}
%\newcommand{\acm@teaser}{}
%\newcommand{\teaser}[1]{\renewcommand{\acm@teaser}{#1}}
\newlength{\titlespace}
\setlength{\titlespace}{0.25in}
%\newlength{\teaserspace}
%\setlength{\teaserspace}{0.25in}
%\ifacm@review
%    \renewcommand{\@maketitle}{%
%        \begin{center}%
%            \renewcommand{\thanks}[1]{}
%            {\LARGE\sffamily\bfseries\acm@sectionfont \@title \par}%
%            \vspace{1\baselineskip}%
%            {Category: \acm@category \par}%
%            \vspace{\titlespace}%
%            \ifx\acm@teaser\acm@empty \else%
%                \begingroup%
%                    \def\@captype{figure}%
%                    \acm@teaser%
%                \endgroup\par%
%                \vspace{\teaserspace}%
%            \fi%
%        \end{center} \par%
%    }
%\else
   \renewcommand{\@maketitle}{%
      \begin{center}%
        {\LARGE\sffamily\acm@sectionfont \@title \par}%
        \vspace{1\baselineskip}%
        \large
        \begin{tabular}[t]{c}%
          \@author        \end{tabular}\par%
        \vspace{\titlespace}%
         \@date
      \end{center} \par%
      }
%\fi
%\let\acm@origmaketitle\maketitle
%\let\acm@origand\and
%\renewcommand{\maketitle}{%
%    \let\acm@title\@title%
 %   \let\acm@author\@author%
 %   \acm@origmaketitle%
 %   \thispagestyle{empty}%
%   \ifacm@doublespaced%
 %       \renewcommand{\baselinestretch}{1.66}\selectfont%
 %   \fi
%}
\newtoks\acm@abs
\ifacm@review
    \long\def\acm@add#1{\global\acm@abs\expandafter{\the\acm@abs#1}}
    \long\def\acm@collect{%
        \global\acm@abs{}%
        \let\abstract\acm@@collect
        \abstract
    }
    \long\def\acm@@collect#1\end#2{%
        \def\@tempa{#2}%
        \ifx\@tempa\@currenvir
            \acm@add{#1}%
            \edef\abstract{\noexpand\end{\@tempa}}%
        \else
            \acm@add{#1\end{#2}}%
        \fi
        \abstract
    }
    \newcommand{\acm@modify}{%
        \let\acm@origabs\abstract%
        \let\acm@origendabs\endabstract%
        \renewenvironment{abstract}%
            {\acm@collect}%
            {\begingroup
                \let\abstract\acm@origabs
                \let\endabstract\acm@origendabs
                \begin{abstract} \the\acm@abs \end{abstract}
            \endgroup}%
    }
    \AtBeginDocument{\acm@modify}
\fi
\newcommand{\keywordlist}{%
    \vspace{0.5\baselineskip}%
    \par\noindent \textbf{Keywords: } \acm@keywords%
}
\newenvironment{CRcatlist}{%
    \vspace{0.5\baselineskip}%
    \par\noindent \textbf{CR Categories: }%
}{}
\newcommand{\CRcat}[4]{%
    #1 [#2]%
    \ifx#3\acm@empty \else : #3\fi%
    \ifx#4\acm@empty \else ---#4\fi%
}
\newlength{\acm@copyrightlength}
%\ifnum\acm@specversion=1994
%    \setlength{\acm@copyrightlength}{1in}
%\else
%    \setlength{\acm@copyrightlength}{1.5in}
%\fi
\newcommand{\copyrightspace}{%
    \renewcommand{\thefootnote}{}%
    \footnotetext[0]{\rule[\acm@copyrightlength]{2.71828in}{0in}}%
    \renewcommand{\thefootnote}{\arabic{footnote}}
}
\renewcommand{\footnoterule}{%
    \kern-3pt
    \hrule width 0.45\columnwidth
    \kern 2.6pt}
\newcommand{\acm@contactname}{}
\newcommand{\contactname}[1]{\renewcommand{\acm@contactname}{#1}}
\newcommand{\acm@contactaddress}{}
\newcommand{\contactaddress}[1]{\renewcommand{\acm@contactaddress}{#1}}
\newcommand{\acm@contactphone}{}
\newcommand{\contactphone}[1]{\renewcommand{\acm@contactphone}{#1}}
\newcommand{\acm@contactfax}{}
\newcommand{\contactfax}[1]{\renewcommand{\acm@contactfax}{#1}}
\newcommand{\acm@contactemail}{}
\newcommand{\contactemail}[1]{\renewcommand{\acm@contactemail}{#1}}
\newcommand{\passport}[1]{%
  \ClassWarningNoLine{myclass}{%
    You no longer need to specify which author should \MessageBreak%
    receive a free conference passport when submitting \MessageBreak%
    papers for review.\MessageBreak%
    The passport command has therefore been disabled}}
\newcommand{\acmpassport}[1]{\passport{#1}}
\newcommand{\acm@keywords}{}
\newcommand{\keywords}[1]{\renewcommand{\acm@keywords}{#1}}
\newcommand{\acm@estpages}{}
\newcommand{\estpages}[1]{\renewcommand{\acm@estpages}{#1}}
\newif\ifacm@cover
\ifacm@review
    \acm@covertrue
\else
    \acm@coverfalse
\fi
\newcommand{\suppresscover}{\acm@coverfalse}
\newcommand{\acm@coverpage}{%
    \begin{titlepage}%
        \def\thanks##1{}
        \let\and\acm@origand
        \acm@setninepoint\normalsize
        \renewcommand{\baselinestretch}{1}\selectfont
        \begin{center}%
            \vspace*{\fill}
            {\LARGE\sffamily\bfseries\acm@sectionfont \acm@title \par}%
            \vspace{2\baselineskip}%
            {\large
                \begin{tabular}[t]{c}%
                \acm@author
             \end{tabular}\par%
            }%
            \vspace{1\baselineskip}%
            {\large \acm@affiliation \par}%
            \addvspace{3\baselineskip}%
            {Category: \acm@category \par}%
            \vspace{0.5\baselineskip}%
            {Format: \acm@format \par}%
            \vspace{3\baselineskip}%
            \begin{tabular}{ll}
                Contact: & \acm@contactname \\[1\baselineskip]
                         & \begin{tabular}[b]{@{}l@{}}
                               \acm@contactaddress
                               \end{tabular} \\[1\baselineskip]
                phone: & \acm@contactphone \\
                fax: & \acm@contactfax \\
                email: & \acm@contactemail
            \end{tabular}\par%
            \vspace*{3\baselineskip}%
            {Estimated \# of pages: \acm@estpages \par}%
            \vspace*{\baselineskip}%
            {Keywords: \acm@keywords \par}%
            \vspace*{\fill}%
            \begin{minipage}{5in}%
                \the\acm@abs
            \end{minipage}\par%
            \vspace*{\fill}
        \end{center}%
    \end{titlepage}%
}

%% This definitions go in conjunction with the amsmath package
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}{Lemma}[section]
\newtheorem{corollary}{Corollary}[section]
\newtheorem{claim}{Claim}[section]
\newtheorem{prop}{Proposition}[section]
\newtheorem{fact}{Fact}[section]
\newtheorem{problem}{Problem}[section]
\numberwithin{equation}{section}
\newtheorem{defn}{Definition}[section]
\newenvironment{proofsketch}{\par{\textbf{Proof Sketch:}}}{\(\qed\) \par}


%%%%% Always use this at end of includes, since definitions are
%%%%% overwritten by hyperref. 
%%%%%
%%%%% Also make sure to specify pdftex/dvips/dvipdfm in the document
%%%%% class header, so that the \special commands are set up properly
\newcommand{\hyperrefmode}[1]{\usepackage[letterpaper,#1]{hyperref}}
% \usepackage[section]{algorithm}
% \usepackage{algorithmic}



\AtEndDocument{\ifacm@cover \acm@coverpage \fi}
\InputIfFileExists{myclass.cfg}
        {\typeout{***************************************^^J%
                  * Local config file myclass.cfg used *^^J%
                  ***************************************}}
        {}
\endinput
%%
%% End of file `myclass.cls'.

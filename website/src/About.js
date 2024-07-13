const About = (props) => {
    const language = props.language === 'pt' ? 1 : 0

    const texts = [
        {
            title: "About the Project",
            introd: "Why do you love your favorite playlist? What truly matters to you in a song? Would you like to discover more music in the same style? This project aims to answer these questions and allows you to listen to more of what you truly enjoy but haven't discovered yet.",
            explain: "spotify-multiverse is a full-stack application that helps users discover new songs based on a playlist they already love. Through mathematical analysis, the project extracts the essential elements of the user's favorite songs, enabling the search for other tracks that will also be appealing. By leveraging concepts from linear algebra, such as vector and matrix operations, the application identifies patterns in the user's playlist and matches them with similar songs in the Spotify database.",
            disclaimer: "Errors may occur due to issues with the Spotify API.",
            credits: "Final Project in Scientific Computing and Data Analysis, by Hugo Folloni"
        },
        {
            title: "Sobre o Projeto",
            introd: "Por que você gosta da sua playlist preferida? O que realmente importa em uma música pra você? Você gostaria de conhecer mais músicas nesse mesmo estilo? Este projeto ajuda a responder algumas dessas perguntas e permite que você ouça mais do que realmente gosta, mas ainda não conhece.",
            explain: "O spotify-multiverse é um aplicativo full-stack que ajuda os usuários a descobrir novas músicas com base em uma playlist que eles já amam. Por meio de análises matemáticas, o projeto extrai os elementos essenciais das músicas favoritas do usuário, permitindo a busca por outras faixas que também serão agradáveis. Utilizando conceitos de álgebra linear, como operações com vetores e matrizes, o aplicativo identifica padrões na playlist do usuário e os compara com músicas semelhantes no banco de dados do Spotify.",
            disclaimer: "Podem ocorrer erros devido a problemas com a API do Spotify.",
            credits: "Projeto Final de Computação Científica e Análise de Dados, feito por Hugo Folloni"
        }
    ]

    return ( 
        <div className="about-div">
            <h1>{texts[language].title}</h1>
            <span>{texts[language].introd}</span>
            <span>{texts[language].explain}</span>
            <h3>Disclaimer</h3>
            <span>{texts[language].disclaimer}</span>
            <p className="credits">{texts[language].credits}</p>
        </div>
     );
}
 
export default About;

use std::{fs, path::Path};

use clap::{Parser, Subcommand};
use serde_yaml;
use serde::{Deserialize, Serialize};

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Cli {
    verb: String,
    #[clap(subcommand)]
    tense: Option<Tense>,
    field: Option<String>,
}

#[derive(Parser, Debug)]
struct TenseArgs {
    pronoun: Option<String>,
}

#[derive(Subcommand, Debug)]
enum Tense {
    #[clap(name = "presente", about = "Conjugations for Presente Indicativo")]
    PresenteIndicativo(TenseArgs),

    #[clap(name = "preterito", about = "Conjugations for Preterito Perfecto Simple")]
    PreteritoPerfectoSimple(TenseArgs),

    #[clap(name = "imperfecto", about = "Conjugations for Preterito Imperfecto")]
    PreteritoImperfecto(TenseArgs),

    #[clap(name = "futuro", about = "Conjugations for Futuro Simple")]
    FuturoSimple(TenseArgs),

    #[clap(name = "condicional", about = "Conjugations for Condicional Simple")]
    CondicionalSimple(TenseArgs),

    #[clap(name = "pres-perf", about = "Conjugations for Presente Perfecto")]
    PresentePerfecto(TenseArgs),

    #[clap(name = "pret-plus", about = "Conjugations for Preterito Pluscuamperfecto")]
    PreteritoPluscuamperfecto(TenseArgs),

    #[clap(name = "fut-perf", about = "Conjugations for Futuro Perfecto")]
    FuturoPerfecto(TenseArgs),

    #[clap(name = "cond-perf", about = "Conjugations for Condicional Perfecto")]
    CondicionalPerfecto(TenseArgs),

    #[clap(name = "pres-subj", about = "Conjugations for Presente Subjuntivo")]
    PresenteSubjuntivo(TenseArgs),

    #[clap(name = "pret-perf-subj", about = "Conjugations for Preterito Perfecto Subjuntivo")]
    PreteritoPerfectoSubjuntivo(TenseArgs),

    #[clap(name = "imp-subj", about = "Conjugations for Imperfecto Subjuntivo")]
    ImperfectoSubjuntivo(TenseArgs),

    #[clap(name = "plus-subj", about = "Conjugations for Pluscuamperfecto Subjuntivo")]
    PluscuamperfectoSubjuntivo(TenseArgs),

    #[clap(name = "imperativo", about = "Conjugations for Imperativo")]
    Imperativo(TenseArgs),
}


#[derive(Debug, Serialize, Deserialize)]
struct VerbConjugation {
    meaning: String,
    infinitivo: String,
    gerundio: String,
    #[serde(rename = "participio-pasado")]
    participio_pasado: String,
    #[serde(rename = "presente-indicativo")]
    presente_indicativo: Conjugation,
    #[serde(rename = "preterito-perfecto-simple")]
    preterito_perfecto_simple: Conjugation,
    #[serde(rename = "preterito-imperfecto")]
    preterito_imperfecto: Conjugation,
    #[serde(rename = "futuro-simple")]
    futuro_simple: Conjugation,
    #[serde(rename = "condicional-simple")]
    condicional_simple: Conjugation,
    #[serde(rename = "presente-perfecto")]
    presente_perfecto: Conjugation,
    #[serde(rename = "preterito-pluscuamperfecto")]
    preterito_pluscuamperfecto: Conjugation,
    #[serde(rename = "futuro-perfecto")]
    futuro_perfecto: Conjugation,
    #[serde(rename = "condicional-perfecto")]
    condicional_perfecto: Conjugation,
    #[serde(rename = "presente-subjuntivo")]
    presente_subjuntivo: Conjugation,
    #[serde(rename = "preterito-perfecto-subjuntivo")]
    preterito_perfecto_subjuntivo: Conjugation,
    #[serde(rename = "imperfecto-subjuntivo")]
    imperfecto_subjuntivo: ConjugationWithAlternatives,
    #[serde(rename = "pluscuamperfecto-subjuntivo")]
    pluscuamperfecto_subjuntivo: ConjugationWithAlternatives,
    imperativo: ImperativeConjugation,
}

#[derive(Debug, Serialize, Deserialize)]
struct Conjugation {
    yo: String,
    tu: String,
    vos: String,
    ud: String,
    nosotros: String,
    vosotros: String,
    uds: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct ConjugationWithAlternatives {
    yo: Vec<String>,
    tu: Vec<String>,
    vos: Vec<String>,
    ud: Vec<String>,
    nosotros: Vec<String>,
    vosotros: Vec<String>,
    uds: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct ImperativeConjugation {
    tu: String,
    vos: String,
    ud: String,
    nosotros: String,
    vosotros: String,
    uds: String,
}

fn handle_tense(conjugation: &Conjugation, args: TenseArgs) {
    if let Some(pronoun) = args.pronoun {
        match pronoun.as_str() {
            "yo" => println!("{}", conjugation.yo),
            "tu" => println!("{}", conjugation.tu),
            "vos" => println!("{}", conjugation.vos),
            "ud" => println!("{}", conjugation.ud),
            "nosotros" => println!("{}", conjugation.nosotros),
            "vosotros" => println!("{}", conjugation.vosotros),
            "uds" => println!("{}", conjugation.uds),
            _ => println!("Invalid pronoun specified."),
        }
    } else {
        println!("{:#?}", conjugation);
    }
}

fn handle_tense_with_alternatives(conjugation: &ConjugationWithAlternatives, args: TenseArgs) {
    if let Some(pronoun) = args.pronoun {
        match pronoun.as_str() {
            "yo" => println!("{:?}", conjugation.yo),
            "tu" => println!("{:?}", conjugation.tu),
            "vos" => println!("{:?}", conjugation.vos),
            "ud" => println!("{:?}", conjugation.ud),
            "nosotros" => println!("{:?}", conjugation.nosotros),
            "vosotros" => println!("{:?}", conjugation.vosotros),
            "uds" => println!("{:?}", conjugation.uds),
            _ => println!("Invalid pronoun specified."),
        }
    } else {
        println!("{:#?}", conjugation);
    }
}

fn handle_imperative_tense(conjugation: &ImperativeConjugation, args: TenseArgs) {
    if let Some(pronoun) = args.pronoun {
        match pronoun.as_str() {
            "tu" => println!("{}", conjugation.tu),
            "vos" => println!("{}", conjugation.vos),
            "ud" => println!("{}", conjugation.ud),
            "nosotros" => println!("{}", conjugation.nosotros),
            "vosotros" => println!("{}", conjugation.vosotros),
            "uds" => println!("{}", conjugation.uds),
            _ => println!("Invalid pronoun specified."),
        }
    } else {
        println!("{:#?}", conjugation);
    }
}

fn main() -> eyre::Result<()> {
    let args = Cli::parse();

    let filepath = format!("verbs/{}.yml", args.verb);
    println!("Loading verb file: {}", filepath);
    if !Path::new(&filepath).exists() {
        eyre::bail!("The specified verb file does not exist.");
    }

    let file_contents = fs::read_to_string(filepath)?;
    let verb_conjugation: VerbConjugation = serde_yaml::from_str(&file_contents)?;

    if let Some(field) = args.field {
        match field.as_str() {
            "meaning" => println!("{}", verb_conjugation.meaning),
            "gerundio" => println!("{}", verb_conjugation.gerundio),
            "participio-pasado" => println!("{}", verb_conjugation.participio_pasado),
            _ => println!("Invalid field specified."),
        }
    } else if let Some(tense) = args.tense {
        match tense {
            Tense::PresenteIndicativo(args) => handle_tense(&verb_conjugation.presente_indicativo, args),
            Tense::PreteritoPerfectoSimple(args) => handle_tense(&verb_conjugation.preterito_perfecto_simple, args),
            Tense::PreteritoImperfecto(args) => handle_tense(&verb_conjugation.preterito_imperfecto, args),
            Tense::FuturoSimple(args) => handle_tense(&verb_conjugation.futuro_simple, args),
            Tense::CondicionalSimple(args) => handle_tense(&verb_conjugation.condicional_simple, args),
            Tense::PresentePerfecto(args) => handle_tense(&verb_conjugation.presente_perfecto, args),
            Tense::PreteritoPluscuamperfecto(args) => handle_tense(&verb_conjugation.preterito_pluscuamperfecto, args),
            Tense::FuturoPerfecto(args) => handle_tense(&verb_conjugation.futuro_perfecto, args),
            Tense::CondicionalPerfecto(args) => handle_tense(&verb_conjugation.condicional_perfecto, args),
            Tense::PresenteSubjuntivo(args) => handle_tense(&verb_conjugation.presente_subjuntivo, args),
            Tense::PreteritoPerfectoSubjuntivo(args) => handle_tense(&verb_conjugation.preterito_perfecto_subjuntivo, args),
            Tense::ImperfectoSubjuntivo(args) => handle_tense_with_alternatives(&verb_conjugation.imperfecto_subjuntivo, args),
            Tense::PluscuamperfectoSubjuntivo(args) => handle_tense_with_alternatives(&verb_conjugation.pluscuamperfecto_subjuntivo, args),
            Tense::Imperativo(args) => handle_imperative_tense(&verb_conjugation.imperativo, args),
        }
    }

    Ok(())
}

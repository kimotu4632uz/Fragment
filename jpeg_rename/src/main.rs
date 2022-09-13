use exif::{Reader, Tag, In};
use glob::glob;
use chrono::{Local, DateTime, TimeZone};
use anyhow::Result;

use std::fs;
use std::path::{Path, PathBuf};
use std::io;
use std::io::Write;
use std::default::Default;
use std::env;
use std::time::SystemTime;

fn getname<P: AsRef<Path>>(p: P) -> Result<PathBuf> {
	let path: &Path = p.as_ref();
    let file = fs::File::open(path)?;
    let mut bufreader = io::BufReader::new(&file);
    let reader = Reader::new();
    let exif = reader.read_from_container(&mut bufreader)?;
    
    let name: String = exif
        .get_field(Tag::DateTimeOriginal, In::PRIMARY).unwrap()
        .value.display_as(Tag::DateTimeOriginal).to_string()
        .chars().filter(|x| x.is_numeric()).collect();
    
    let ext = path.extension().unwrap_or(Default::default());
    
    Ok(path.with_file_name(name).with_extension(ext))
}

fn main() -> Result<()> {
    let dir = env::args().nth(1).expect("Error: no argument supplied");
    let file = Path::new(&dir);
    let ext = file.extension().unwrap();
    let unix_time = file.metadata()?.created()?.duration_since(SystemTime::UNIX_EPOCH)?.as_millis();
    let datetime = Local.timestamp_millis(unix_time.try_into().unwrap());
    let new_name = file.with_file_name(datetime.format("%Y%m%d%H%M%S").to_string()).with_extension(ext);
    println!("{} -> {}", file.display(), new_name.display());
    print!("Do you want to continue? [Y/n] ");
    io::stdout().flush().unwrap();

    let mut buf = String::new();
    io::stdin().read_line(&mut buf)?;
    if buf.starts_with("Y") || buf.starts_with("y") {
        fs::rename(file, new_name)?;
    } else {
        println!("Aborted.");
    }

    //let dir_glob = Path::new(&dir).join("*");
    //for file in glob(dir_glob.to_str().unwrap()).unwrap().filter_map(Result::ok) {
    //    //fs::rename(file, getname(file))?;
    //    let unix_time = file.metadata()?.created()?.duration_since(SystemTime::UNIX_EPOCH)?.as_millis();
    //    let datetime = Local.timestamp_millis(unix_time.try_into().unwrap());
    //    println!("{}", datetime.format("%Y%m%d%H%M%S"));
    //}
    Ok(())
}

import { useEffect, useState } from "react"
import { useResolvedPath } from "react-router-dom"
import { fileExtensions } from "../icons/supportedExtensions.ts"
import { folderExtensions } from "../icons/supportedFolders.ts"
// import { folderExtensions } from "@/icons/supportedFolders"

function getFileIcon(filename) {
    // console.log("=========================")
    // console.log(filename)

    let icon;

    for (let k of fileExtensions.supported) {
        if (k.disabled) { continue; }

        if (k.extensionsGlob && k.filenamesGlob) {
            for (let _ext of k.extensionsGlob) {
                for (let _filename of k.filenamesGlob) {
                    if (filename.startsWith(_filename) && filename.endsWith(_ext)) {
                        // console.log(k.icon)
                        icon = "/icons/file_type_" + k.icon + ".svg"
                        // return "/icons/file_type_" + k.icon + ".svg"
                    }
                }
            }
        }
        if (k?.extensions) {
            for (let ext of k?.extensions) {
                if (k.filename) {
                    if (filename == ext) {
                        // console.log(k.icon)
                        icon = "/icons/file_type_" + k.icon + ".svg"
                        // return "/icons/file_type_" + k.icon + ".svg"
                    }
                } else if (filename.endsWith("." + ext)) {
                    // console.log(k.icon)
                    icon = "/icons/file_type_" + k.icon + ".svg"
                    // return "/icons/file_type_" + k.icon + ".svg"
                }
            }
        }
        if (k?.languages) {
            for (let ext of k?.languages) {
                if (k.filename) {
                    if (filename == ext) {
                        // console.log(k.icon)
                        icon = "/icons/file_type_" + k.icon + ".svg"
                        // return "/icons/file_type_" + k.icon + ".svg"
                    }
                } else if (filename.endsWith("." + ext.defaultExtension)) {
                    // console.log(k.icon)
                    icon = "/icons/file_type_" + k.icon + ".svg"
                    // return "/icons/file_type_" + k.icon + ".svg"
                }
            }
        }
    }
    // console.log("=========================")
    return icon
}

function getFolderIcon(filename) {
    for (let k of folderExtensions.supported) {
        if (k.disabled) { continue; }
        if (k?.extensions) {
            for (let ext of k?.extensions) {
                if (filename == ext) {
                    return "/icons/folder_type_" + k.icon + ".svg"
                }
            }
        }
    }
}

function File({ file }) {

    let icon = getFileIcon(file.filename)

    if (!icon) {
        icon = "/icons/default_file.svg"
    }

    return (
        <Content file={file} icon={icon} />
    )
}

function Directory({ file }) {
    const path = useResolvedPath()

    let icon = getFolderIcon(file.filename)

    if (!icon) {
        icon = "/icons/default_folder.svg"
    }
    return (
        <a href={path.pathname + "/" + file.filename}>
            <Content file={file} icon={icon} />
        </a>
    )
}

function Content({ file, icon }) {
    return (
        <div className="text-white hover:bg-neutral-600 h-6 m-2 rounded-md grid gap-3" style={{ gridTemplateColumns: "24px 1fr 100px 300px" }}>
            <img src={icon} className="h-6" alt=""></img>
            <label>{file.filename}</label>
            <label>{file.size} B</label>
            <label>{file.date_modified}</label>
        </div>
    )
}

export default function MainContainer() {

    const path = useResolvedPath()
    const [contents, setContents] = useState([]);

    useEffect(() => {

        if (path.pathname.endsWith("/")) {
            window.location.pathname = window.location.pathname.slice(0, -1)
        }

        let dir_path
        if (path.pathname == "/files") {
            dir_path = "/"
        } else {
            dir_path = "/" + path.pathname.replace("/files/", "")
        }

        fetch("/api/get-directory" + dir_path).then(reponse => reponse.json().then(data => {
            setContents(data)
        }))
    }, [path])

    return (
        <div className="h-full w-full bg-neutral-900 ">
            <div className="absolute top-5 left-5 right-10 bottom-4 overflow-y-auto">
                {contents.map(file => {
                    if (file.type === "directory") {
                        return <Directory key={file.filename} file={file} />

                    } else {
                        return <File key={file.filename} file={file} />
                    }
                })}
            </div>
        </div>
    )
}
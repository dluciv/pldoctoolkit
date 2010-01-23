#include "import.h"
#include "publishutil.h"

VoidT importDocLineDoc()
{
	F_ObjHandleT docID;
	StringT dirPath, tmpPath, bookPath;
	FilePathT *filedirPath, *file;
	DirHandleT handle;
	IntT statusp;
	F_PropValsT params, *returnParams;

	returnParams = NULL;
	params = generateOpenParams();
	docID = F_ApiOpen(defaultPath,&params,&returnParams);
	if (!docID)
	{
		F_Printf(NULL,"No such file: %s\n", defaultPath);
		return;
	}
	dirPath = F_ApiGetString(FV_SessionId,docID,FP_Name);
	F_ApiClose(docID,FF_CLOSE_MODIFIED);
	params = generateImportParams();
	pathFilename(dirPath);//since then dirPath should be const
	filedirPath = F_PathNameToFilePath (dirPath, NULL, FDosPath);//since then filedirPath should be const
	if (!performImportXSLT(dirPath)) return;
	if (!cleanImportDirectory(dirPath)) return;
	bookPath = "";
	handle = F_FilePathOpenDir(filedirPath,&statusp);
	if (!handle)
	{
		F_Printf(NULL,"import error:\n\tInvalid directory path: %s\n",dirPath);
		return;
	}
	//Opening of all .drl files in directory with structured application "DocLine"
	while((file = F_FilePathGetNext(handle, &statusp)) != NULL)
	{
		tmpPath = F_FilePathToPathName(file,FDosPath);
		importBook(tmpPath,params);
	}
	F_FilePathCloseDir(handle);
	openFilesInDirectory(dirPath);
	cleanDirectory(filedirPath);

	F_Free(&docID);
	F_Free(&handle);
	F_Free(&statusp);
	F_ApiDeallocatePropVals(&params);    
	F_ApiDeallocatePropVals(returnParams);
	F_FilePathFree(filedirPath);
	F_FilePathFree(file);
	F_ApiDeallocateString(&dirPath);
	F_ApiDeallocateString(&bookPath);
	F_ApiDeallocateString(&tmpPath);
}

BoolT importBook(StringT path, F_PropValsT params)
{
	F_ObjHandleT fileID, elemID;
	F_AttributeT attr;
	F_AttributesT attrs;
	F_PropValsT *returnParams;
	UIntT j;

	if (!validateFilename(path,DRL)) return 0;
	returnParams = NULL;
	fileID = F_ApiOpen(path,&params,&returnParams);
	if (!fileID)
	{
		F_Printf(NULL,"Error in opening file %s",path);
		return 0;
	}
	elemID = F_ApiGetId(FV_SessionId,fileID,FP_HighestLevelElement);
	//Inserting additional attribute, that indicates file name, in highest level element
	if ((F_StrIEqual(F_ApiGetString(fileID,F_ApiGetId(fileID,elemID,FP_ElementDef),FP_Name),(StringT)"DocumentationCore"))||
		(F_StrIEqual(F_ApiGetString(fileID,F_ApiGetId(fileID,elemID,FP_ElementDef),FP_Name),(StringT)"ProductLine"))||
		(F_StrIEqual(F_ApiGetString(fileID,F_ApiGetId(fileID,elemID,FP_ElementDef),FP_Name),(StringT)"ProductDocumentation")))
	{
		attrs = F_ApiGetAttributes(fileID,elemID);
		for (j=0; j<attrs.len; j++)
		{
			attr = attrs.val[j];
			if (F_StrIEqual(attr.name,(StringT)"FileName"))
			{
				if (!attr.values.len)
				{
					attr.values.len = 1;
					attr.values.val = (StringT*)F_Alloc(sizeof(StringT),DSE);
				}
				attr.values.val[0] = fileFileName(F_StrCopyString(path));
				attrs.val[j] = attr;
			}
		}
		F_ApiSetAttributes(fileID,elemID,&attrs);
	}
	renameFilesToActualNames(fileID);
	fileID = F_ApiSimpleSave(fileID,F_ApiGetString(FV_SessionId,fileID,FP_Name),False);
	F_ApiClose(fileID,FF_CLOSE_MODIFIED);

	F_Free(&fileID);
	F_Free(&elemID);
	F_ApiDeallocatePropVals(returnParams);
	F_ApiDeallocateAttributes(&attrs);
	//F_ApiDeallocateAttribute(&attr);//was commented

	return 1;
}
BoolT performImportXSLT(StringT dirPath)
{
	IntT retVal;
	UCharT jarPath[256];
	StringT tempPath;

	tempPath = F_ApiClientDir();
	F_Sprintf(jarPath, "%s\\%s", tempPath, JAR_FILENAME);
	retVal = callJavaImportUtil(jarPath, dirPath);
	if (retVal > 0)
	{
		F_Printf(NULL,"JVM Initiliazation error\n");

	}

	F_Free(&jarPath);
	F_ApiDeallocateString(&tempPath);

	return !retVal;
}

BoolT cleanImportDirectory(StringT dirPath)
{
	FilePathT *filedirPath, *file;
	DirHandleT handle;
	StringT tmpPath;
	IntT statusp;

	filedirPath = F_PathNameToFilePath (dirPath, NULL, FDosPath);
	handle = F_FilePathOpenDir(filedirPath, &statusp);
	if (!handle)
	{
		F_FilePathFree(filedirPath);
		F_ApiAlert("Handle Error2", FF_ALERT_CONTINUE_NOTE);
		return 0;
	}
	//Deleting non-docline files in directory
	while (file = F_FilePathGetNext(handle,&statusp))
	{
		tmpPath = F_FilePathToPathName(file,FDosPath);
		if (!validateFilename(tmpPath,DRL))
		{
			F_DeleteFile(file);
		}
	}
	F_FilePathCloseDir(handle);

	F_Free(&handle);
	F_ApiDeallocateString(&tmpPath);
	F_Free(&statusp);
	F_FilePathFree(file);
	F_FilePathFree(filedirPath);

	return 1;
}
VoidT openFilesInDirectory(StringT path)
{
	FilePathT *newpath, *file;
	StringT bookPath, tmpPath;
	//path - path of openned document
	//newpath~path
	//bookPath - book path
	//defaultPath - default directory path
	F_ObjHandleT bookID, compID, elemID;
	DirHandleT handle;
	IntT statusp;
	BoolT compExists;

	pathFilename(path);
	if (!(bookID = openMainBook(path))) return;
	if (!addExistingDocs(path,bookID)) return;
	newpath = F_PathNameToFilePath (path, NULL, FDosPath);
	compID = F_ApiGetId(FV_SessionId,bookID,FP_FirstComponentInBook);
	while (compID)
	{
		compExists = False;
		handle = F_FilePathOpenDir(newpath,&statusp);
		if (!handle)
		{
			F_Printf(NULL,"OpenDir:\n\tDirectory error: %s\n", F_FilePathToPathName(newpath,FDosPath));
			return;
		}
		while (file = F_FilePathGetNext(handle,&statusp))
		{
			tmpPath = F_FilePathToPathName(file,FDosPath);
			if (compExists = F_StrIEqual(fileFileName(tmpPath),fileFileName(F_ApiGetString(bookID,compID,FP_Name))))
			{
				break;
			}
		}
		if (!compExists)
		{
			elemID = F_ApiGetId(bookID,compID,FP_NextComponentInBook);
			F_ApiDelete(bookID,compID);
			compID = elemID;
		}
		else
		{
			compID = F_ApiGetId(bookID,compID,FP_NextComponentInBook);
		}
		F_FilePathCloseDir(handle);
	}
	bookPath = F_ApiGetString(FV_SessionId,bookID,FP_Name);
	F_ApiSimpleGenerate(bookID,False,True);
	F_ApiSimpleSave(bookID,bookPath,False); 

	F_ApiDeallocateString(&bookPath);
	F_Free(&elemID);
	F_ApiDeallocateString(&tmpPath);
	F_FilePathFree(file);
	F_Free(&statusp);
	F_Free(&handle);
	F_Free(&compExists);
	F_Free(&compID);
	F_FilePathFree(newpath);
	F_Free(&bookID);
}
VoidT openBook()
{
	StringT path;
	F_ObjHandleT docID;
	//Do not use russian letters in path!!!
	docID = F_ApiSimpleOpen(defaultPath,True);
	if (!docID)
	{
		F_Printf(NULL,"No such file: %s\n",defaultPath);
		return;
	}
	path = F_FilePathToPathName(F_PathNameToFilePath(F_ApiGetString(FV_SessionId,docID,FP_Name),NULL,FDefaultPath),FDosPath);
	if ((!validateFilename(path,FM))&&(!((validateFilename(path,FMBOOK))&&(F_StrISuffix(path,defaultBookName)))))
	{
		F_Printf(NULL,"Error. Not Framemaker file\n");
		return;
	}
	pathFilename(path);
	openFilesInDirectory(path);
}
F_PropValsT generateOpenParams()
{
	F_PropValsT params;
	IntT i;

	params = F_ApiGetOpenDefaultParams();
	if (!params.len)
	{
		F_ApiAlert("Default params error",FF_ALERT_CONTINUE_NOTE);
	}
	i = F_ApiGetPropIndex(&params, FS_ShowBrowser);
	params.val[i].propVal.u.ival = True;
	i = F_ApiGetPropIndex(&params, FS_ForceOpenAsText);
	params.val[i].propVal.u.ival = True;

	F_Free(&i);

	return params;
}
F_PropValsT generateImportParams()
{
	F_PropValsT params;
	IntT i;

	params = F_ApiGetOpenDefaultParams();
	if (!params.len)
	{
		F_ApiAlert("Default params error",FF_ALERT_CONTINUE_NOTE);
	}
	i = F_ApiGetPropIndex(&params,FS_StructuredOpenApplication);
	params.val[i].propVal.u.sval = "DocLine";

	F_Free(&i);

	return params;
}
VoidT renameFilesToActualNames(F_ObjHandleT bookID)
{
	F_ObjHandleT compID;
	StringT compPath, newCompPath, dirPath;
	F_AttributesT attrs;
	F_AttributeT attr;
	UIntT i, j;

	if (!bookID)
	{
		F_Printf(NULL,"renameFilesToActualNames error:\n\tInvalid Book\n");
		return;
	}
	dirPath = F_ApiGetString(FV_SessionId,bookID,FP_Name);
	pathFilename(dirPath);
	compID = F_ApiGetId(FV_SessionId,bookID,FP_FirstComponentInBook);
	while (compID)
	{
		compPath = F_ApiGetString(bookID,compID,FP_Name);
		attrs = F_ApiGetAttributes(bookID,F_ApiGetId(bookID,compID,FP_ComponentElement));
		for (j=0; j<attrs.len; j++)
		{
			attr = attrs.val[j];
			if (F_StrIEqual(attr.name,(StringT)"Id"))
			{
				if (!attr.values.len)
				{
					F_Printf(NULL,"Error in Id attribute in %s\n",compPath);
					continue;
				}

				newCompPath = F_Alloc(F_StrLen(attr.values.val[0])+F_StrLen(dirPath)+10,NO_DSE);
				F_Sprintf(newCompPath,"%s%s.fm",dirPath,attr.values.val[0]);
				i = 0;
				while (F_RenameFile(F_PathNameToFilePath(compPath,NULL,FDosPath),F_PathNameToFilePath(newCompPath,NULL,FDosPath)) != FdeSuccess)
				{
					F_Sprintf(newCompPath,"%s%s%d.fm",dirPath,attr.values.val[0],i);
					F_Printf(NULL,"%s\n",newCompPath);
					i++;
				}
				F_ApiSetString(bookID,compID,FP_Name,newCompPath);
				F_ApiDeallocateString(&newCompPath);
			}
		}
		compID = F_ApiGetId(bookID,compID,FP_NextComponentInBook);
	}

	F_Free(&compID);
	//F_ApiDeallocateAttribute(&attr);
	F_ApiDeallocateAttributes(&attrs);
	F_ApiDeallocateString(&compPath);
	F_ApiDeallocateString(&dirPath);
	F_Free(&i);
	F_Free(&j);
}

VoidT simpleOpenBook()
{
	StringT filePath;
	F_ObjHandleT bookID;

	bookID = F_ApiSimpleOpen(defaultPath,True);
	if (!bookID) return;
	filePath = F_ApiGetString(FV_SessionId,bookID,FP_Name);
	filePath = fileFileName(filePath);
	if (!F_StrIEqual(filePath,defaultBookName))
	{
		F_ApiClose(bookID,FF_CLOSE_MODIFIED);
	}
	F_ApiDeallocateString(&filePath);
	F_Free(&bookID);
}
BoolT addExistingDocs(StringT path, F_ObjHandleT bookID)
{
	DirHandleT handle;
	IntT statusp;
	FilePathT *file, *filepath;
	StringT tmpPath;

	filepath = F_PathNameToFilePath (path, NULL, FDosPath);
	handle = F_FilePathOpenDir(filepath, &statusp);
	if (!handle)
	{
		F_Printf(NULL,"OpenBooks:\n\tDirectory path error: %s\n",path);
		return 0;
	}
	while((file = F_FilePathGetNext(handle, &statusp)))
	{
		tmpPath = F_FilePathToPathName(file, FDosPath);
		if (validateFilename(tmpPath,FM)) 
		{
			if (!addExistingDoc(tmpPath,bookID)) return 0;
		}
		else if ((!F_StrIEqual(fileFileName(tmpPath),defaultBookName))&&
			(!validateFilename(tmpPath,FMBOOK))&&
			(!validateFilename(tmpPath,DRL)))
		{
			F_DeleteFile(file);
		}
	}

	F_FilePathCloseDir(handle);
	F_Free(&statusp);
	F_ApiDeallocateString(&tmpPath);
	F_FilePathFree(file);
	F_FilePathFree(filepath);
	F_Free(&handle);

	return 1;
}
BoolT addExistingDoc(StringT path, F_ObjHandleT bookID)
{
	F_ObjHandleT compID, docID, elemID;
	BoolT compExists;
	StringT tmpPath2, fileName, place;
	F_ElementLocT elemLoc;

	compID = F_ApiGetId(FV_SessionId,bookID,FP_FirstComponentInBook);
	compExists = False;
	while ((compID != 0)&&(!compExists))
	{
		tmpPath2 = F_ApiGetString(bookID,compID,FP_Name);
		compExists =  F_StrIEqual(fileFileName(path),fileFileName(tmpPath2));
		compID = F_ApiGetId(bookID,compID,FP_NextComponentInBook);
	}
	if (!compExists)
	{
		docID = F_ApiSimpleOpen(path,False);
		fileName = getHighestString(docID);
		F_ApiClose(docID,FF_CLOSE_MODIFIED);
		place = getPlace(fileName);
		if (F_StrIEqual(place,(StringT)""))
		{
			compID = F_ApiNewSeriesObject(bookID,FO_BookComponent,0);
			F_ApiSetString(bookID,compID,FP_Name,path);
		}
		else
		{
			compID = F_ApiGetId(FV_SessionId,bookID,FP_HighestLevelElement);
			//compID = F_ApiGetId(bookID,F_ApiGetId(FV_SessionId,bookID,FP_MainFlowInDoc),FP_HighestLevelElement);
			if (!compID)
			{
				F_Printf(NULL,"OpenFiles:\n\tHighest element error\n");
				return 0;
			}
			else
			{
				compID = componentExists(bookID,compID,place);
				if (!compID)
				{
					elemID = F_ApiGetNamedObject(bookID,FO_ElementDef,place);
					elemLoc.parentId = F_ApiGetId(FV_SessionId,bookID,FP_HighestLevelElement);
					elemLoc.childId = 0;
					elemLoc.offset = 0;
					compID = F_ApiNewElementInHierarchy(bookID,elemID,&elemLoc);
				}
				elemLoc.parentId = compID;
				elemLoc.offset = 0;
				elemLoc.childId = 0;
				compID = F_ApiNewBookComponentInHierarchy(bookID,path,&elemLoc);
			}
		}
	}

	F_Free(&compID);
	F_Free(&elemLoc);
	F_Free(&elemID);
	F_ApiDeallocateString(&place);
	F_ApiDeallocateString(&fileName);
	F_Free(&docID);
	F_Free(&compExists);
	F_ApiDeallocateString(&tmpPath2);//

	return 1;
}
